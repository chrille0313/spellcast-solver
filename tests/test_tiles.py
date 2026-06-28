import pytest

from spellcast_solver.tiles import Bonus, Tile


def test_value_derived_from_letter():
    assert Tile("q").value == 8
    assert Tile("a").value == 1


def test_value_override_wins():
    assert Tile("a", value=5).value == 5


def test_letter_is_normalised():
    assert Tile("e").letter == "E"


def test_bad_letter_rejected():
    with pytest.raises(ValueError):
        Tile("ab")


def test_bonus_multipliers():
    assert Bonus.DOUBLE_LETTER.letter_multiplier == 2
    assert Bonus.TRIPLE_LETTER.letter_multiplier == 3
    assert Bonus.DOUBLE_WORD.word_multiplier == 2
    assert Bonus.TRIPLE_WORD.word_multiplier == 3
    assert Bonus.DOUBLE_LETTER.word_multiplier == 1
    assert Bonus.NONE.letter_multiplier == 1


@pytest.mark.parametrize(
    "token,expected",
    [("dl", Bonus.DOUBLE_LETTER), ("2L", Bonus.DOUBLE_LETTER),
     ("TW", Bonus.TRIPLE_WORD), ("", Bonus.NONE)],
)
def test_bonus_parse(token, expected):
    assert Bonus.parse(token) == expected
