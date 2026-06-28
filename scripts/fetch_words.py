"""Download a word list into data/words.txt.

SpellCast's exact dictionary is not published, so this uses a standard
Scrabble-style word list, which is a close match in practice. Swap in any
newline-delimited list of uppercase words if you have a better source.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt"
TARGET = Path(__file__).resolve().parent.parent / "data" / "words.txt"


def main() -> int:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {SOURCE_URL}")
    with urllib.request.urlopen(SOURCE_URL) as response:
        TARGET.write_bytes(response.read())
    count = sum(1 for _ in TARGET.open(encoding="utf-8"))
    print(f"Wrote {count} words to {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
