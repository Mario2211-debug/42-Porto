"""Per-prompt orchestration of the whole pipeline."""

from ..models import FunctionCall, FunctionDefinition
from .generation_loop import GenerationLoop, LanguageModel
from .output_parser import OutputParser, OutputParserError
from .prompt_builder import PromptBuilder
from .schema_grammar import SchemaGrammar
from .vocab_map import VocabMap


class FunctionCallerError(Exception):
    """Raised when one prompt fails to yield a usable function call."""

    def __init__(self, prompt: str, reason: str) -> None:
        """Keeps the offending prompt around so the caller can report it."""
        self.prompt = prompt
        self.reason = reason
        super().__init__(f"Failed to process prompt {prompt!r}: {reason}")


class FunctionCaller:
    """Turns a natural language request into a validated function call."""

    def __init__(
        self,
        model: LanguageModel,
        vocab_map: VocabMap,
        functions: list[FunctionDefinition],
        max_steps: int = 256,
    ) -> None:
        """Builds the pipeline once, to be reused across prompts.

        Args:
            model: Object exposing the LLM SDK interface.
            vocab_map: Vocabulary of the same model.
            functions: Functions the model may choose from.
            max_steps: Safety bound on decoding iterations per prompt.
        """
        self.functions = functions
        self.prompt_builder = PromptBuilder()
        self.generation_loop = GenerationLoop(
            model=model, vocab_map=vocab_map, max_steps=max_steps
        )
        self.output_parser = OutputParser()

    def call(self, user_prompt: str) -> FunctionCall:
        """Runs the full pipeline for a single prompt.

        A fresh :class:`SchemaGrammar` is built per prompt so no state ever
        leaks from one request into the next.

        Args:
            user_prompt: The natural language request.

        Returns:
            The function call the model chose.

        Raises:
            FunctionCallerError: If generation or validation fails.
        """
        grammar = SchemaGrammar(self.functions)
        prompt = self.prompt_builder.build(user_prompt, self.functions)

        try:
            generated = self.generation_loop.generate(prompt, grammar)
        except (RuntimeError, ValueError) as exc:
            raise FunctionCallerError(user_prompt, str(exc)) from exc

        try:
            return self.output_parser.parse(
                user_prompt, generated,
                function_definition=grammar.chosen_function,
            )
        except OutputParserError as exc:
            raise FunctionCallerError(user_prompt, str(exc)) from exc
