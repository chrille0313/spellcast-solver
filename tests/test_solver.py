from pathlib import Path

from spellcast_solver.board import Board
from spellcast_solver.solver import Solver
from spellcast_solver.tiles import Bonus, Tile
from spellcast_solver.trie import Trie

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_keeps_highest_scoring_path_for_a_word():
    # TOT can be spelled two ways; only the route through the double-word O
    # should be reported.
    board = Board([
        [Tile("T"), Tile("O")],
        [Tile("O", Bonus.DOUBLE_WORD), Tile("T")],
    ])
    trie = Trie.from_words(["TOT"])
    moves = Solver(board, trie, min_length=3).solve()
    assert len(moves) == 1
    assert moves[0].word == "TOT"
    assert moves[0].score == (2 + 1 + 2) * 2


def test_min_length_filters_short_words():
    board = Board([[Tile("T"), Tile("O"), Tile("T")]])
    trie = Trie.from_words(["TO", "TOT"])
    words = {m.word for m in Solver(board, trie, min_length=3).solve()}
    assert words == {"TOT"}


def test_no_tile_is_reused_in_a_path():
    # A single A tile cannot spell AA.
    board = Board([[Tile("A"), Tile("B")]])
    trie = Trie.from_words(["AA"])
    assert Solver(board, trie, min_length=2).solve() == []


def test_redeye_is_the_best_play_on_the_example_board():
    board = Board.parse((EXAMPLES / "board_redeye.txt").read_text(encoding="utf-8"))
    trie = Trie.from_words(["REDEYE", "DECKER", "BACKER", "DICKER"])
    moves = Solver(board, trie, min_length=3).solve()
    best = moves[0]
    assert best.word == "REDEYE"
    assert best.score == 66
    assert best.is_long_word


def test_keddah_is_the_best_play_on_the_example_board():
    board = Board.parse((EXAMPLES / "board_keddah.txt").read_text(encoding="utf-8"))
    trie = Trie.from_words(["KEDDAH", "CARRIED", "CHIEF"])
    best = Solver(board, trie, min_length=3).solve()[0]
    assert best.word == "KEDDAH"
    assert best.score == 56
