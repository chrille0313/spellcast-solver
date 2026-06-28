"""Loading the word list and building a trie from it."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

from .trie import Trie

DEFAULT_WORDS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "words.txt"


def iter_words(path: Path, min_length: int = 2) -> Iterator[str]:
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            word = line.strip().upper()
            if len(word) >= min_length and word.isalpha():
                yield word


def load_trie(path: Path | None = None, min_length: int = 2) -> Trie:
    path = path or DEFAULT_WORDS_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"word list not found at {path}. Run scripts/fetch_words.py to download one, "
            "or pass --words PATH."
        )
    return Trie.from_words(iter_words(path, min_length=min_length))
