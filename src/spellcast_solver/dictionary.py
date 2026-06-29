"""Loading the word list and building a trie from it.

The package bundles the public-domain ENABLE word list, so ``load_trie()``
works with no setup. Pass a path to use your own list instead.
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import Iterable, Iterator

from .trie import Trie

BUNDLED_WORDS = "data/enable.txt"


def iter_words(lines: Iterable[str], min_length: int = 2) -> Iterator[str]:
    for line in lines:
        word = line.strip().upper()
        if len(word) >= min_length and word.isalpha():
            yield word


def load_trie(path: str | Path | None = None, min_length: int = 2) -> Trie:
    """Build a trie from a word list.

    With no ``path``, the bundled ENABLE list is used. Otherwise ``path`` must
    point to a file with one word per line.
    """
    if path is None:
        resource = files("spellcast_solver").joinpath(BUNDLED_WORDS)
        with resource.open("r", encoding="utf-8") as handle:
            return Trie.from_words(iter_words(handle, min_length=min_length))

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"word list not found at {path}")
    with open(path, encoding="utf-8") as handle:
        return Trie.from_words(iter_words(handle, min_length=min_length))
