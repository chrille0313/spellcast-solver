"""Depth-first search over the board, guided by the trie."""

from __future__ import annotations

from dataclasses import dataclass

from .board import Board
from .trie import Trie, TrieNode


@dataclass(frozen=True)
class Move:
    word: str
    path: list[tuple[int, int]]
    score: int
    gems: int

    @property
    def is_long_word(self) -> bool:
        return len(self.word) >= 6


class Solver:
    def __init__(self, board: Board, trie: Trie, min_length: int = 3) -> None:
        self.board = board
        self.trie = trie
        self.min_length = min_length

    def solve(self) -> list[Move]:
        """Return every reachable word, best score first.

        A word can be spelled by several paths; we keep the highest-scoring
        path for each word.
        """
        best: dict[str, Move] = {}
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                start = self.trie.root.children.get(self.board.tile(r, c).letter)
                if start is not None:
                    self._dfs(r, c, start, [(r, c)], {(r, c)}, best)
        return sorted(best.values(), key=lambda m: (-m.score, -len(m.word), m.word))

    def _dfs(
        self,
        r: int,
        c: int,
        node: TrieNode,
        path: list[tuple[int, int]],
        visited: set[tuple[int, int]],
        best: dict[str, Move],
    ) -> None:
        if node.word is not None and len(node.word) >= self.min_length:
            score = self.board.score_path(path)
            current = best.get(node.word)
            if current is None or score > current.score:
                best[node.word] = Move(
                    word=node.word,
                    path=list(path),
                    score=score,
                    gems=self.board.gems_on_path(path),
                )
        for nr, nc in self.board.neighbours(r, c):
            if (nr, nc) in visited:
                continue
            child = node.children.get(self.board.tile(nr, nc).letter)
            if child is None:
                continue
            visited.add((nr, nc))
            path.append((nr, nc))
            self._dfs(nr, nc, child, path, visited, best)
            path.pop()
            visited.remove((nr, nc))
