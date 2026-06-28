"""Tiles, bonuses, and the canonical SpellCast letter values."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

# Official SpellCast letter point values, per the Discord wiki:
# https://discord.fandom.com/wiki/SpellCast
# Any individual tile value can be overridden via Tile(value=...).
LETTER_VALUES: dict[str, int] = {
    "A": 1, "E": 1, "I": 1, "O": 1,
    "N": 2, "R": 2, "S": 2, "T": 2,
    "D": 3, "G": 3, "L": 3,
    "B": 4, "H": 4, "M": 4, "P": 4, "U": 4, "Y": 4,
    "C": 5, "F": 5, "V": 5, "W": 5,
    "K": 6,
    "J": 7, "X": 7,
    "Q": 8, "Z": 8,
}


class Bonus(Enum):
    """A tile bonus. Letter bonuses scale one tile; word bonuses scale the
    whole word and stack multiplicatively when more than one is on a path."""

    NONE = ""
    DOUBLE_LETTER = "DL"
    TRIPLE_LETTER = "TL"
    DOUBLE_WORD = "DW"
    TRIPLE_WORD = "TW"

    @property
    def letter_multiplier(self) -> int:
        return {Bonus.DOUBLE_LETTER: 2, Bonus.TRIPLE_LETTER: 3}.get(self, 1)

    @property
    def word_multiplier(self) -> int:
        return {Bonus.DOUBLE_WORD: 2, Bonus.TRIPLE_WORD: 3}.get(self, 1)

    @classmethod
    def parse(cls, token: str) -> "Bonus":
        token = token.strip().upper()
        if not token:
            return cls.NONE
        aliases = {
            "2L": cls.DOUBLE_LETTER, "DL": cls.DOUBLE_LETTER,
            "3L": cls.TRIPLE_LETTER, "TL": cls.TRIPLE_LETTER,
            "2W": cls.DOUBLE_WORD, "DW": cls.DOUBLE_WORD,
            "3W": cls.TRIPLE_WORD, "TW": cls.TRIPLE_WORD,
        }
        if token not in aliases:
            raise ValueError(f"unknown bonus {token!r}")
        return aliases[token]


@dataclass(frozen=True)
class Tile:
    """A single board cell.

    ``value`` defaults to the canonical value for ``letter`` but can be
    overridden for boards that show a different number.
    """

    letter: str
    bonus: Bonus = Bonus.NONE
    gem: bool = False
    value: int | None = None

    def __post_init__(self) -> None:
        letter = self.letter.strip().upper()
        if len(letter) != 1 or not letter.isalpha():
            raise ValueError(f"tile letter must be a single A-Z, got {self.letter!r}")
        object.__setattr__(self, "letter", letter)
        if self.value is None:
            object.__setattr__(self, "value", LETTER_VALUES[letter])
