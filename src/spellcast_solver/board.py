"""The board: a grid of tiles plus adjacency and scoring."""

from __future__ import annotations

from typing import Iterator

from .tiles import Bonus, Tile

# Scoring rules (Discord SpellCast).
LONG_WORD_MIN_LENGTH = 6
LONG_WORD_BONUS = 10

_NEIGHBOUR_OFFSETS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]


class Board:
    def __init__(self, tiles: list[list[Tile]]) -> None:
        if not tiles or not tiles[0]:
            raise ValueError("board must have at least one tile")
        width = len(tiles[0])
        if any(len(row) != width for row in tiles):
            raise ValueError("all board rows must be the same width")
        self.tiles = tiles
        self.rows = len(tiles)
        self.cols = width

    def tile(self, r: int, c: int) -> Tile:
        return self.tiles[r][c]

    def neighbours(self, r: int, c: int) -> Iterator[tuple[int, int]]:
        for dr, dc in _NEIGHBOUR_OFFSETS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield nr, nc

    def score_path(self, path: list[tuple[int, int]]) -> int:
        """Score a path under SpellCast rules.

        Letter bonuses scale individual tiles; word bonuses multiply the whole
        word and stack. The long-word bonus is added after multiplication, so
        word multipliers do not apply to it.
        """
        letter_total = 0
        word_multiplier = 1
        for r, c in path:
            tile = self.tiles[r][c]
            letter_total += tile.value * tile.bonus.letter_multiplier
            word_multiplier *= tile.bonus.word_multiplier
        score = letter_total * word_multiplier
        if len(path) >= LONG_WORD_MIN_LENGTH:
            score += LONG_WORD_BONUS
        return score

    def gems_on_path(self, path: list[tuple[int, int]]) -> int:
        return sum(1 for r, c in path if self.tiles[r][c].gem)

    @classmethod
    def parse(cls, text: str) -> "Board":
        """Parse a text board.

        One row per line; whitespace-separated cells. Each cell is a letter
        optionally followed by ``/BONUS`` (DL, TL, DW, TW) and/or ``*`` to mark
        a gem. Order of the bonus and gem markers does not matter.

            D    E/TL  Y/DW  E   E/DL
            E    I/DL  C     A/DL E
            T    R/DW  K     A/TL A/DL
            A    E     G     E    B
            B*   S     E     W*   J
        """
        rows: list[list[Tile]] = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            rows.append([_parse_cell(tok) for tok in line.split()])
        return cls(rows)


def _parse_cell(token: str) -> Tile:
    gem = "*" in token
    token = token.replace("*", "")
    letter, _, bonus_token = token.partition("/")
    return Tile(letter=letter, bonus=Bonus.parse(bonus_token), gem=gem)
