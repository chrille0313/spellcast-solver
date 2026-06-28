# spellcast-solver

A solver for the Discord SpellCast word game. Give it a board and it finds the
highest-scoring words you can spell by linking adjacent tiles.

## How it works

SpellCast is a path-finding word game: you spell a word by stepping between
tiles that touch (including diagonally), using each tile at most once, and you
score letter values modified by bonus tiles.

The solver does a depth-first search over the board, but the key idea is that
the search is **guided by a trie** built from the dictionary. The DFS over the
grid and the descent through the trie are the same traversal:

- Each tile you step onto follows one child edge of the current trie node.
- If that child does not exist, no word continues down this path, so the whole
  branch is pruned instantly.
- Terminal trie nodes carry the full word, so a match never has to rebuild the
  string it spelled.

This is both cleaner and cheaper than checking a prefix set: extending a path is
an O(1) child lookup instead of rebuilding and re-hashing the prefix string at
every step, and the trie shares prefixes instead of storing a separate string
for each one.

## Install

```bash
pip install -e .
python scripts/fetch_words.py   # downloads data/words.txt
```

The word list is not committed (it is large and has its own licensing). SpellCast
does not publish its exact dictionary, so the fetch script pulls a standard
Scrabble-style list, which is a close match. Point `--words` at any other
newline-delimited list if you have a better one.

## Usage

```bash
spellcast-solve examples/board_redeye.txt --top 10
```

Output is best score first, with the path and any bonuses applied:

```
  66  REDEYE           R(2,1) -> E(1,0) -> D(0,0) -> E(0,1) -> Y(0,2) -> E(0,3)  [long]
```

### Board format

One row per line, whitespace-separated cells. Each cell is a letter, optionally
followed by `/BONUS` and/or `*` for a gem tile. Bonus codes: `DL`, `TL`, `DW`,
`TW` (or `2L`, `3L`, `2W`, `3W`). Lines starting with `#` are comments.

```
D     E/TL  Y/DW  E     E/DL
E     I/DL  C     A/DL  E
T     R/DW  K     A/TL  A/DL
A     E     G     E     B
B     S     E     W     J
```

### Library

```python
from spellcast_solver import Board, Solver, load_trie

board = Board.parse(open("examples/board_redeye.txt").read())
solver = Solver(board, load_trie())
moves = solver.solve()
print(moves[0].word, moves[0].score)
```

## Scoring

- Each letter has a fixed point value (see `LETTER_VALUES` in `tiles.py`).
- `DL` / `TL` multiply a single tile's value by 2 / 3.
- `DW` / `TW` multiply the whole word by 2 / 3 and stack multiplicatively.
- Words of six letters or more get a flat +10 long-word bonus, added after the
  word multiplier (so the multiplier does not apply to the bonus).

Letter values are taken directly from the official SpellCast scoring table (see
Sources). Any tile value can still be overridden if your board shows something
different.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Sources

- [Discord Wiki: SpellCast](https://discord.fandom.com/wiki/SpellCast) (letter values and scoring rules)

## License

MIT
