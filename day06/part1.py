import argparse
import sys
from collections import defaultdict
from typing import Dict, List

import pytest


def walk(matrix: Dict[str, Dict[str, int]], x: str, steps: int) -> None:
    if x not in matrix:
        return

    steps += 1
    for y, v in matrix[x].items():
        matrix[x][y] = steps
        walk(matrix, y, steps)


def calc(lines: str) -> int:
    matrix: Dict[str, Dict[str, int]] = defaultdict(dict)
    for line in lines.strip().split("\n"):
        left, right = line.split(")")
        matrix[left][right] = 0

    walk(matrix, "COM", 0)

    return sum(matrix[x][y] for x in matrix for y in matrix[x])


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)

    print(calc(args.infile.read()))

    return 0


@pytest.mark.parametrize("s, expected", (("COM)B\nB)C\nB)G", 5),))
def test(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
