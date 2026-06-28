"""A prefix trie over the word list.

The solver walks this trie in lockstep with its walk over the board: stepping
to a neighbouring tile is a single O(1) child lookup, and a missing child
prunes that whole branch of the search immediately. Terminal nodes store the
full word so the solver never has to rebuild the string it spelled.
"""

from __future__ import annotations

from typing import Iterable, Optional


class TrieNode:
    __slots__ = ("children", "word")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        # The complete word if a word ends here, else None.
        self.word: Optional[str] = None


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.word = word

    def __contains__(self, word: str) -> bool:
        node = self.root
        for ch in word:
            node = node.children.get(ch)
            if node is None:
                return False
        return node.word is not None

    @classmethod
    def from_words(cls, words: Iterable[str]) -> "Trie":
        trie = cls()
        for word in words:
            trie.insert(word)
        return trie
