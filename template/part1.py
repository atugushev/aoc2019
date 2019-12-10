import argparse
import sys
from typing import List

import pytest


def solve(lines: str) -> int:
    pass


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


@pytest.mark.parametrize(
    "s, expected",
    (
        # test cases
        ("", None),
        ("", None),
        ("", None),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
