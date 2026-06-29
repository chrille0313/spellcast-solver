"""A solver for the Discord SpellCast word game."""

from .board import Board
from .dictionary import load_trie
from .solver import Move, Solver
from .tiles import Bonus, Tile
from .trie import Trie

__all__ = ["Board", "Bonus", "Move", "Solver", "Tile", "Trie", "load_trie"]
__version__ = "1.0.1"
