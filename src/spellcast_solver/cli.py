"""Command-line entry point: solve a board from a file or stdin."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .board import Board
from .dictionary import load_trie
from .solver import Move, Solver


def _format_path(board: Board, move: Move) -> str:
    return " -> ".join(
        f"{board.tile(r, c).letter}({r},{c})" for r, c in move.path
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="spellcast-solve",
        description="Find the highest-scoring words on a SpellCast board.",
    )
    parser.add_argument(
        "board",
        nargs="?",
        type=Path,
        help="path to a board file (reads stdin if omitted)",
    )
    parser.add_argument("--words", type=Path, default=None, help="path to a word list")
    parser.add_argument("--top", type=int, default=10, help="how many results to show")
    parser.add_argument(
        "--min-length", type=int, default=3, help="ignore words shorter than this"
    )
    args = parser.parse_args(argv)

    text = args.board.read_text(encoding="utf-8") if args.board else sys.stdin.read()
    board = Board.parse(text)
    trie = load_trie(args.words)
    moves = Solver(board, trie, min_length=args.min_length).solve()

    if not moves:
        print("No words found.")
        return 0

    for move in moves[: args.top]:
        flags = []
        if move.is_long_word:
            flags.append("long")
        if move.gems:
            flags.append(f"{move.gems} gem{'s' if move.gems > 1 else ''}")
        suffix = f"  [{', '.join(flags)}]" if flags else ""
        print(f"{move.score:4d}  {move.word:<15}  {_format_path(board, move)}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
