from spellcast_solver.trie import Trie


def test_insert_and_contains():
    trie = Trie.from_words(["CAT", "CAR", "CARD"])
    assert "CAT" in trie
    assert "CAR" in trie
    assert "CARD" in trie


def test_prefix_is_not_a_word():
    trie = Trie.from_words(["CARD"])
    assert "CAR" not in trie
    # but the prefix path exists for the search to descend
    node = trie.root
    for ch in "CAR":
        node = node.children[ch]
    assert node.word is None


def test_terminal_stores_word():
    trie = Trie.from_words(["DOG"])
    node = trie.root
    for ch in "DOG":
        node = node.children[ch]
    assert node.word == "DOG"


def test_missing_word():
    trie = Trie.from_words(["CAT"])
    assert "DOG" not in trie
