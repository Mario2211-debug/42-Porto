"""Token id to text mapping, plus pre-computed candidate pools.

The decoder has to answer "which of the 150k tokens are legal here?" once per
generated token. Doing that by scanning every token with the grammar would
dominate the runtime, so this class pre-computes, at load time, the coarse
pools the grammar can then refine:

* tokens grouped by their first character;
* tokens that may appear inside a JSON string literal.

Anything the grammar could never accept — non printable or non ASCII text,
which cannot appear in our JSON output — is dropped entirely at load time.
"""

import json
import string
from collections import defaultdict

import numpy as np

_SPACE_MARKER = "Ġ"

_PRINTABLE_ASCII = frozenset(
    c for c in string.printable if c not in "\t\n\r\x0b\x0c"
)


class VocabMapError(Exception):
    """Raised when the vocabulary file cannot be read or parsed."""


class VocabMap:
    """Maps token ids to their decoded text and exposes candidate pools."""

    def __init__(self, vocab_path: str) -> None:
        """Loads and indexes the tokenizer vocabulary.

        Args:
            vocab_path: Path to the ``vocab.json`` file of the model.

        Raises:
            VocabMapError: If the file is missing or is not valid JSON.
        """
        self._id_to_token: dict[int, str] = self._load_vocab(vocab_path)
        if not self._id_to_token:
            raise VocabMapError(f"No usable tokens found in {vocab_path!r}.")

        self._all_ids = np.fromiter(self._id_to_token, dtype=np.int64)
        self._ids_by_first_char = self._index_by_first_char()

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    @classmethod
    def _load_vocab(cls, vocab_path: str) -> dict[int, str]:
        """Reads ``vocab.json`` and keeps only tokens usable in JSON output."""
        try:
            with open(vocab_path, "r", encoding="utf-8") as vocab_file:
                raw_vocab: dict[str, int] = json.load(vocab_file)
        except OSError as exc:
            raise VocabMapError(
                f"Could not read vocabulary file {vocab_path!r}: {exc}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise VocabMapError(
                f"Vocabulary file {vocab_path!r} is not valid JSON: {exc}"
            ) from exc

        id_to_token: dict[int, str] = {}
        for raw_token, token_id in raw_vocab.items():
            text = raw_token.replace(_SPACE_MARKER, " ")
            if text and all(c in _PRINTABLE_ASCII for c in text):
                id_to_token[int(token_id)] = text
        return id_to_token

    def _index_by_first_char(self) -> dict[str, np.ndarray]:
        """Groups token ids by the first character of their text."""
        grouped: dict[str, list[int]] = defaultdict(list)
        for token_id, text in self._id_to_token.items():
            grouped[text[0]].append(token_id)
        return {char: np.array(ids, dtype=np.int64)
                for char, ids in grouped.items()}

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def decode_token(self, token_id: int) -> str:
        """Returns the text of *token_id*, or ``""`` if it was filtered out."""
        return self._id_to_token.get(token_id, "")

    def all_ids(self) -> np.ndarray:
        """Ids of every usable token."""
        return self._all_ids

    def ids_for_first_chars(self, first_chars: set[str]) -> np.ndarray:
        """Ids of every token whose text starts with one of *first_chars*."""
        groups = [self._ids_by_first_char[char] for char in first_chars
                  if char in self._ids_by_first_char]
        if not groups:
            return np.empty(0, dtype=np.int64)
        return np.concatenate(groups)

    def vocab_size(self) -> int:
        """Number of usable tokens kept after filtering."""
        return len(self._id_to_token)
