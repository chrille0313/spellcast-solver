from spellcast_solver.board import LONG_WORD_BONUS, Board
from spellcast_solver.tiles import Bonus, Tile


def _row(*tiles):
    return list(tiles)


def test_plain_score_is_sum_of_values():
    # C(5) A(1) T(2)
    board = Board([_row(Tile("C"), Tile("A"), Tile("T"))])
    assert board.score_path([(0, 0), (0, 1), (0, 2)]) == 8


def test_double_letter_scales_one_tile():
    board = Board([_row(Tile("C", Bonus.DOUBLE_LETTER), Tile("A"), Tile("T"))])
    assert board.score_path([(0, 0), (0, 1), (0, 2)]) == 5 * 2 + 1 + 2


def test_double_word_scales_whole_word():
    board = Board([_row(Tile("C", Bonus.DOUBLE_WORD), Tile("A"), Tile("T"))])
    assert board.score_path([(0, 0), (0, 1), (0, 2)]) == (5 + 1 + 2) * 2


def test_word_multipliers_stack():
    board = Board([_row(Tile("C", Bonus.DOUBLE_WORD), Tile("A", Bonus.DOUBLE_WORD), Tile("T"))])
    assert board.score_path([(0, 0), (0, 1), (0, 2)]) == (5 + 1 + 2) * 4


def test_long_word_bonus_added_after_multiplier():
    # Six 1-point tiles with a double word: (6 * 2) + 10, not (6 + 10) * 2.
    tiles = [Tile("A", Bonus.DOUBLE_WORD)] + [Tile("E") for _ in range(5)]
    board = Board([tiles])
    path = [(0, i) for i in range(6)]
    assert board.score_path(path) == 6 * 2 + LONG_WORD_BONUS


def test_diagonal_neighbours():
    board = Board([_row(Tile("A"), Tile("B")), _row(Tile("C"), Tile("D"))])
    assert set(board.neighbours(0, 0)) == {(0, 1), (1, 0), (1, 1)}


def test_parse_reads_bonuses_and_gems():
    board = Board.parse("A/DL* B\nC D/DW")
    assert board.tile(0, 0).bonus == Bonus.DOUBLE_LETTER
    assert board.tile(0, 0).gem is True
    assert board.tile(1, 1).bonus == Bonus.DOUBLE_WORD
    assert board.gems_on_path([(0, 0), (0, 1)]) == 1
