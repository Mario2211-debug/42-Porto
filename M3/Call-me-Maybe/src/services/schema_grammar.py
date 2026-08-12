"""Incremental JSON grammar used to constrain the decoder.

The grammar is a cursor over a list of :class:`GrammarStep` objects that
together describe the only JSON document we are willing to produce::

    {"name": "<one of the declared functions>", "parameters": {...}}

It answers two questions for the decoder:

* :meth:`SchemaGrammar.is_token_valid` — could this token text appear here
  without ever breaking JSON syntax or the declared schema?
* :meth:`SchemaGrammar.advance` — consume the chosen token and move on.

Because the parameter list depends on which function the model picks, the
steps after the function name are built lazily, the moment the name is known.
"""

import re
import string
from dataclasses import dataclass
from typing import NamedTuple, Optional

from ..models import FunctionDefinition, GrammarStep, ParamType, StepType

DEFAULT_MAX_STRING_LENGTH = 200

DEFAULT_MAX_NUMBER_LENGTH = 24

_NUMBER_PREFIX = re.compile(r'^-?((0|[1-9]\d*)(\.\d*)?)?$')
_NUMBER_FULL = re.compile(r'^-?(0|[1-9]\d*)(\.\d+)?$')
_INTEGER_PREFIX = re.compile(r'^-?(0|[1-9]\d*)?$')
_INTEGER_FULL = re.compile(r'^-?(0|[1-9]\d*)$')

_NUMERIC_CHARS = "-.0123456789"

_SIMPLE_ESCAPES = '"\\/bfnrt'


@dataclass
class _State:
    """Mutable cursor over the step list.

    A copy of this is used to *simulate* a candidate token without touching
    the real state, which is what makes :meth:`SchemaGrammar.is_token_valid`
    side-effect free.
    """

    steps: list[GrammarStep]
    index: int
    buffer: str
    chosen: Optional[FunctionDefinition]
    owns_steps: bool

    def clone(self) -> "_State":
        """Returns a copy that may mutate its own step list freely."""
        return _State(
            steps=self.steps,
            index=self.index,
            buffer=self.buffer,
            chosen=self.chosen,
            owns_steps=False,
        )


class JsonStringScan(NamedTuple):
    """What a partially generated JSON string literal looks like so far."""

    valid: bool
    """False once the text can no longer become a well-formed string."""

    terminated: bool
    """True once the closing quote has been consumed."""

    escape_pending: bool
    """True when the text stops inside an unfinished ``\\`` escape."""

    length: int
    """Characters the string decodes to; a pending escape counts as none."""


_INVALID_SCAN = JsonStringScan(False, False, False, 0)


def scan_json_string(buffer: str) -> JsonStringScan:
    """Validates a partially generated JSON string literal.

    Args:
        buffer: Text accumulated so far, expected to start with a quote.

    Returns:
        A :class:`JsonStringScan` describing the text.
    """
    if not buffer.startswith('"'):
        if '"'.startswith(buffer):
            return JsonStringScan(True, False, False, 0)
        return _INVALID_SCAN

    i = 1
    size = len(buffer)
    length = 0
    while i < size:
        char = buffer[i]
        if char == '"':
            # Nothing may follow the closing quote inside this step.
            return JsonStringScan(i == size - 1, True, False, length)
        if char == '\\':
            if i + 1 >= size:
                return JsonStringScan(True, False, True, length)
            escaped = buffer[i + 1]
            if escaped == 'u':
                digits = buffer[i + 2:i + 6]
                if not all(c in string.hexdigits for c in digits):
                    return _INVALID_SCAN
                if len(digits) < 4:
                    return JsonStringScan(True, False, True, length)
                i += 6
            elif escaped in _SIMPLE_ESCAPES:
                i += 2
            else:
                return _INVALID_SCAN
        elif char < ' ' or char == '\x7f':
            return _INVALID_SCAN              # raw control char
        else:
            i += 1
        length += 1
    return JsonStringScan(True, False, False, length)


class SchemaGrammar:
    """Tracks which token texts keep the generated JSON valid and on-schema."""

    def __init__(
        self,
        functions: list[FunctionDefinition],
        max_string_length: int = DEFAULT_MAX_STRING_LENGTH,
        max_number_length: int = DEFAULT_MAX_NUMBER_LENGTH,
    ) -> None:
        """Builds a grammar for one generation.

        The two length caps exist for termination: digits and string content
        are always locally legal, so without a bound a model that keeps
        picking them would never close the document.

        Args:
            functions: The functions the model is allowed to choose from.
            max_string_length: Cap on string parameter length; once reached,
                only a closing quote is accepted.
            max_number_length: Cap on the number of characters in a numeric
                literal; once reached, only the next step is accepted.

        Raises:
            ValueError: If *functions* is empty; there would be nothing valid
                to generate.
        """
        if not functions:
            raise ValueError("SchemaGrammar needs at least one function.")

        self.functions = functions
        self.functions_by_name = {f.name: f for f in functions}
        self.max_string_length = max_string_length
        self.max_number_length = max_number_length
        self._state = self._initial_state()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def chosen_function(self) -> Optional[FunctionDefinition]:
        """The function the model settled on, once its name is complete."""
        return self._state.chosen

    @property
    def step_index(self) -> int:
        """Index of the step currently being filled (for diagnostics)."""
        return self._state.index

    @property
    def buffer(self) -> str:
        """Text accumulated inside the current step (for diagnostics)."""
        return self._state.buffer

    def is_complete(self) -> bool:
        """True once every step has been filled and the JSON is closed."""
        return self._state.index >= len(self._state.steps)

    def reset(self) -> None:
        """Returns the grammar to its initial state for reuse."""
        self._state = self._initial_state()

    def is_token_valid(self, candidate_text: str) -> bool:
        """True if *candidate_text* keeps the document on-schema.

        The candidate is fed character by character into a throwaway copy of
        the state, so a token is accepted only if *every* character of it is
        legal — including tokens that straddle a step boundary, such as
        ``", "b": `` closing a number and opening the next parameter.
        """
        if not candidate_text or self.is_complete():
            return False

        simulated = self._state.clone()
        for char in candidate_text:
            if not self._feed_char(simulated, char):
                return False
        return True

    def advance(self, chosen_text: str) -> None:
        """Consumes *chosen_text*, moving the cursor forward.

        Raises:
            ValueError: If the text is not valid at the current position;
                the decoder is expected to validate before advancing.
        """
        for char in chosen_text:
            if not self._feed_char(self._state, char):
                raise ValueError(
                    f"Invalid text {chosen_text!r} at step "
                    f"{self._state.index} (buffer={self._state.buffer!r})"
                )

    def is_current_step_forced(self) -> bool:
        """True when there is determined text to emit before the next choice.

        Structural text such as ``{"name": "`` carries no information, so the
        decoder can emit it directly instead of paying for a forward pass.
        """
        return self.forced_prefix() != ""

    def forced_prefix(self) -> str:
        """Returns *all* the text that is determined from here on.

        This deliberately runs past the end of the current step and keeps
        going while the next one is also determined, so a whole structural
        run like ``", "parameters": {"name": "`` comes back as one string.
        That matters for more than speed: the decoder encodes this text in
        one call, and a tokenizer splits ``{"`` into a single token while
        ``{`` followed by ``"name`` gives a sequence the model has hardly
        ever seen. Feeding it unnatural token boundaries measurably degrades
        the values it then produces.

        Returns:
            The determined text, or ``""`` if the next position is a genuine
            choice.
        """
        if self.is_complete():
            return ""

        state = self._state.clone()
        parts: list[str] = []

        while state.index < len(state.steps):
            text = self._determined_text(state)
            if not text:
                break
            parts.append(text)
            for char in text:
                self._feed_char(state, char)

        return "".join(parts)

    def _determined_text(self, state: _State) -> str:
        """Text the step under *state* leaves no choice about."""
        step = state.steps[state.index]

        if step.type == StepType.LITERAL:
            return step.literal_text[len(state.buffer):]

        # The opening quote of a string value is the only legal character
        # there, so it belongs with the structural run before it.
        if (step.type == StepType.PARAM_VALUE
                and step.param_type == ParamType.STRING
                and state.buffer == ""):
            return '"'

        return ""

    def possible_next_first_chars(self) -> Optional[set[str]]:
        """Returns the characters a legal next token may start with.

        Returns None when no useful narrowing exists (inside a string value),
        in which case the decoder falls back to a broader candidate pool.
        """
        if self.is_complete():
            return set()
        return self._first_chars(self._state, depth=0)

    # ------------------------------------------------------------------
    # State machine
    # ------------------------------------------------------------------

    def _initial_state(self) -> _State:
        """Builds the fixed opening steps; parameters are added later."""
        steps = [
            GrammarStep(type=StepType.LITERAL, literal_text='{"name": "'),
            GrammarStep(type=StepType.FUNCTION_NAME_CHOICE),
        ]
        return _State(steps=steps, index=0, buffer="", chosen=None,
                      owns_steps=True)

    def _feed_char(self, state: _State, char: str) -> bool:
        """Feeds one character, closing steps as needed.

        Returns:
            False if the character is illegal at this position.
        """
        if state.index >= len(state.steps):
            return False

        step = state.steps[state.index]

        if self._accepts(step, state.buffer + char):
            state.buffer += char
            if self._must_close(step, state.buffer):
                self._close_step(state)
            return True

        # The character does not fit this step; it may still be legal if the
        # step is allowed to end here and the next one accepts it.
        if self._may_close(step, state.buffer):
            self._close_step(state)
            return self._feed_char(state, char)

        return False

    def _accepts(self, step: GrammarStep, candidate: str) -> bool:
        """True if *candidate* is a valid, possibly partial, value here."""
        if step.type == StepType.LITERAL:
            return step.literal_text.startswith(candidate)

        if step.type == StepType.FUNCTION_NAME_CHOICE:
            return any(name.startswith(candidate)
                       for name in self.functions_by_name)

        return self._accepts_param_value(step, candidate)

    def _accepts_param_value(self, step: GrammarStep, candidate: str) -> bool:
        """Type-specific prefix check for a parameter value."""
        if step.param_type in (ParamType.NUMBER, ParamType.INTEGER):
            is_number = step.param_type == ParamType.NUMBER
            prefix = _NUMBER_PREFIX if is_number else _INTEGER_PREFIX
            if prefix.match(candidate) is None:
                return False
            # A trailing '-' or '.' still owes at least one digit, so leave
            # room for it: reaching the cap owing a digit would be a dead end.
            full = _NUMBER_FULL if is_number else _INTEGER_FULL
            owed = 0 if full.match(candidate) else 1
            return len(candidate) + owed <= self.max_number_length
        if step.param_type == ParamType.BOOLEAN:
            return ("true".startswith(candidate)
                    or "false".startswith(candidate))
        if step.param_type == ParamType.STRING:
            scan = scan_json_string(candidate)
            if not scan.valid or scan.terminated:
                return scan.valid
            # An escape, once started, cannot be abandoned: count the
            # character it is going to become, or the value could reach the
            # cap mid-escape with no legal way to finish.
            pending = 1 if scan.escape_pending else 0
            return scan.length + pending <= self.max_string_length
        return False

    def _must_close(self, step: GrammarStep, buffer: str) -> bool:
        """True when *buffer* can only be a finished value for *step*."""
        if step.type == StepType.LITERAL:
            return buffer == step.literal_text

        if step.type == StepType.FUNCTION_NAME_CHOICE:
            # Only close eagerly when no other function extends this name;
            # with names like fn_add and fn_add_numbers we must keep going
            # and let the closing quote decide.
            if buffer not in self.functions_by_name:
                return False
            return not any(name != buffer and name.startswith(buffer)
                           for name in self.functions_by_name)

        if step.param_type == ParamType.BOOLEAN:
            return buffer in ("true", "false")
        if step.param_type == ParamType.STRING:
            return scan_json_string(buffer).terminated
        return False       # numbers end only when the next step takes over

    def _may_close(self, step: GrammarStep, buffer: str) -> bool:
        """True when *buffer* is already a complete value, but could grow."""
        if step.type == StepType.FUNCTION_NAME_CHOICE:
            return buffer in self.functions_by_name
        if step.type == StepType.PARAM_VALUE:
            if step.param_type == ParamType.NUMBER:
                return _NUMBER_FULL.match(buffer) is not None
            if step.param_type == ParamType.INTEGER:
                return _INTEGER_FULL.match(buffer) is not None
        return False

    def _close_step(self, state: _State) -> None:
        """Finishes the current step and moves the cursor to the next one."""
        step = state.steps[state.index]
        if step.type == StepType.FUNCTION_NAME_CHOICE:
            self._expand_parameter_steps(state)
        state.buffer = ""
        state.index += 1

    def _expand_parameter_steps(self, state: _State) -> None:
        """Inserts the steps for the parameters of the chosen function."""
        function = self.functions_by_name[state.buffer]
        state.chosen = function

        new_steps: list[GrammarStep] = [
            GrammarStep(type=StepType.LITERAL,
                        literal_text='", "parameters": {')
        ]
        new_steps.extend(self._build_parameter_steps(function))

        if not state.owns_steps:
            state.steps = list(state.steps)
            state.owns_steps = True

        insert_at = state.index + 1
        state.steps[insert_at:insert_at] = new_steps

    @staticmethod
    def _build_parameter_steps(
        function: FunctionDefinition,
    ) -> list[GrammarStep]:
        """Builds ``"key": <value>`` steps for every declared parameter."""
        steps: list[GrammarStep] = []

        for position, (name, schema) in enumerate(function.parameters.items()):
            separator = '"' if position == 0 else ', "'
            steps.append(GrammarStep(type=StepType.LITERAL,
                                     literal_text=f'{separator}{name}": '))
            steps.append(GrammarStep(type=StepType.PARAM_VALUE,
                                     param_name=name,
                                     param_type=schema.type))

        steps.append(GrammarStep(type=StepType.LITERAL, literal_text='}}'))
        return steps

    # ------------------------------------------------------------------
    # Candidate narrowing
    # ------------------------------------------------------------------

    def _first_chars(self, state: _State, depth: int) -> Optional[set[str]]:
        """Collects legal first characters, following step boundaries.

        A token may start at the end of one step and continue into the next
        (``, "b": `` after a number), so when the current step is allowed to
        close we also gather the characters that open the following step.
        """
        if depth > 2 or state.index >= len(state.steps):
            return set()

        step = state.steps[state.index]
        chars = self._own_first_chars(step, state.buffer)
        if chars is None:
            return None

        if self._may_close(step, state.buffer):
            after = state.clone()
            self._close_step(after)
            following = self._first_chars(after, depth + 1)
            if following is None:
                return None
            chars = chars | following

        return chars

    def _own_first_chars(self, step: GrammarStep,
                         buffer: str) -> Optional[set[str]]:
        """First characters *step* itself accepts, ignoring its successor."""
        if step.type == StepType.LITERAL:
            remaining = step.literal_text[len(buffer):]
            return {remaining[0]} if remaining else set()

        if step.type == StepType.FUNCTION_NAME_CHOICE:
            return {name[len(buffer)] for name in self.functions_by_name
                    if name.startswith(buffer) and len(name) > len(buffer)}

        if step.param_type == ParamType.BOOLEAN:
            return {option[len(buffer)] for option in ("true", "false")
                    if option.startswith(buffer) and len(option) > len(buffer)}

        if step.param_type in (ParamType.NUMBER, ParamType.INTEGER):
            # Derived from _accepts so the two can never disagree about
            # leading zeros, sign placement or the length cap.
            return {char for char in _NUMERIC_CHARS
                    if self._accepts(step, buffer + char)}

        if step.param_type == ParamType.STRING:
            if buffer == "":
                return {'"'}
            return None        # anything printable may follow

        return set()
