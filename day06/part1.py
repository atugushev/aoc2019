import argparse
import sys
from typing import List

import pytest


def calc(lines: str) -> int:
    pass


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)

    print(calc(args.infile.read()))

    return 0


@pytest.mark.parametrize("s, expected", (("", None)))
def test(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
