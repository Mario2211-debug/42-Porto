"""Token-by-token constrained decoding driver.

This is where constrained decoding actually happens: at every position the
model produces logits over the whole vocabulary, and we discard — that is,
treat as if their logit were minus infinity — every token the grammar refuses.
The model only ever chooses among tokens that keep the output valid, so the
result is guaranteed to parse, no matter how confused the model is.

Two optimisations keep this fast without weakening the guarantee:

1. Purely structural text (``{"name": "``) has a single legal continuation,
   so it is emitted directly instead of paying for a forward pass.
2. At real decision points the grammar narrows the vocabulary to a candidate
   pool before ranking, and the pool is only widened to the full vocabulary
   if nothing in it turns out to be valid.
"""

from typing import Optional, Protocol

import numpy as np

from .schema_grammar import SchemaGrammar
from .vocab_map import VocabMap


class LanguageModel(Protocol):
    """The subset of the LLM SDK this module depends on."""

    def encode(self, text: str) -> object:
        """Encodes text into a tensor of token ids."""

    def decode(self, ids: list[int]) -> str:
        """Decodes token ids back into text."""

    def get_logits_from_input_ids(self, input_ids: list[int]) -> list[float]:
        """Returns next-token logits for the given context."""


class GenerationLoop:
    """Generates one schema-compliant JSON document per call."""

    def __init__(
        self,
        model: LanguageModel,
        vocab_map: VocabMap,
        max_steps: int = 256,
    ) -> None:
        """Wires the decoder to a model and its vocabulary.

        Args:
            model: Object exposing the LLM SDK interface.
            vocab_map: Vocabulary of the same model.
            max_steps: Safety bound on decoding iterations.
        """
        self.model = model
        self.vocab_map = vocab_map
        self.max_steps = max_steps

    def generate(self, prompt: str, grammar: SchemaGrammar) -> str:
        """Runs constrained generation for a single prompt.

        Args:
            prompt: Fully built prompt, already including any chat template.
            grammar: Fresh grammar instance driving the constraints.

        Returns:
            The generated JSON document as text.

        Raises:
            RuntimeError: If no valid token exists for the current state, or
                if the budget runs out before the JSON is closed.
        """
        context: list[int] = self._encode(prompt)
        generated: list[int] = []

        for _ in range(self.max_steps):
            if grammar.is_complete():
                break

            forced = grammar.forced_prefix()
            if forced:
                self._emit_forced_text(forced, grammar, context, generated)
                continue

            token_id = self._select_next_token(context, grammar)
            grammar.advance(self.vocab_map.decode_token(token_id))
            context.append(token_id)
            generated.append(token_id)

        if not grammar.is_complete():
            raise RuntimeError(
                f"Generation did not complete within {self.max_steps} steps."
            )

        return self.model.decode(generated)

    # ------------------------------------------------------------------
    # Forced text (no model consultation needed)
    # ------------------------------------------------------------------

    def _emit_forced_text(
        self,
        text: str,
        grammar: SchemaGrammar,
        context: list[int],
        generated: list[int],
    ) -> None:
        """Appends the only continuation the grammar allows here.

        The whole run is encoded in one call so the tokenizer produces its
        natural boundaries; encoding it piece by piece would hand the model
        a token sequence it has never seen.
        """
        token_ids = self._encode(text)
        context.extend(token_ids)
        generated.extend(token_ids)
        grammar.advance(text)

    def _encode(self, text: str) -> list[int]:
        """Encodes text into a flat list of token ids."""
        encoded = self.model.encode(text)
        ids = encoded.tolist()  # type: ignore[attr-defined]
        return list(ids[0]) if ids and isinstance(ids[0], list) else list(ids)

    # ------------------------------------------------------------------
    # Real decision points (model consultation required)
    # ------------------------------------------------------------------

    def _select_next_token(self, context: list[int],
                           grammar: SchemaGrammar) -> int:
        """Picks the highest-scoring token the grammar accepts.

        Raises:
            RuntimeError: If the whole vocabulary contains no valid token,
                which would mean the grammar is inconsistent.
        """
        logits = np.asarray(
            self.model.get_logits_from_input_ids(context), dtype=np.float64
        )

        token_id = self._best_valid_token(
            self._candidate_pool(grammar), logits, grammar
        )
        if token_id is not None:
            return token_id

        # The narrowed pool failed; never give up before checking everything.
        token_id = self._best_valid_token(
            self.vocab_map.all_ids(), logits, grammar
        )
        if token_id is None:
            raise RuntimeError(
                "No valid token in the vocabulary for the current state "
                f"(step_index={grammar.step_index}, "
                f"buffer={grammar.buffer!r})."
            )
        return token_id

    def _candidate_pool(self, grammar: SchemaGrammar) -> np.ndarray:
        """Returns the ids worth ranking at the current position.

        Inside a string value the answer is "all of them". Narrowing there is
        tempting but wrong: a tokenizer packs the closing quote together with
        what follows it, so ``",`` and ``"}}`` are single tokens — and they
        are exactly how the model naturally ends a value. Excluding them
        leaves only a bare ``"``, which scores far lower, and the model
        rambles on instead of closing.
        """
        first_chars = grammar.possible_next_first_chars()
        if first_chars is None:
            return self.vocab_map.all_ids()
        return self.vocab_map.ids_for_first_chars(first_chars)

    def _best_valid_token(
        self,
        candidate_ids: np.ndarray,
        logits: np.ndarray,
        grammar: SchemaGrammar,
    ) -> Optional[int]:
        """Returns the best-scoring accepted token, or None if there is none.

        Ranking is done with numpy over the whole pool at once; the grammar is
        then consulted in descending score order, so the very first accepted
        token is also the most likely one.
        """
        candidate_ids = candidate_ids[candidate_ids < logits.size]
        if candidate_ids.size == 0:
            return None

        order = np.argsort(-logits[candidate_ids], kind="stable")
        ranked = candidate_ids[order]
        for token_id in ranked:
            text = self.vocab_map.decode_token(int(token_id))
            if grammar.is_token_valid(text):
                return int(token_id)
        return None
