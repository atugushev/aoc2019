import argparse
import sys
from enum import IntEnum
from typing import Dict, List, Tuple

import pytest

from computer import Computer


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HR_PADDLE = 3
    BALL = 4

    @property
    def label(self):
        return "·█▓_●"[self.value]


def solve(lines: str) -> int:
    comp = Computer()
    comp.read_instructions(lines)
    comp.run()

    grid = {}
    blocks = 0

    while comp.stdout:
        t = Tile(comp.stdout.pop())
        y = comp.stdout.pop()
        x = comp.stdout.pop()
        grid[(x, y)] = t

        if t == Tile.BLOCK:
            blocks += 1

    draw(grid)

    return blocks


def draw(panels: Dict[Tuple[int, int], int]) -> None:
    min_x = min(p[0] for p in panels)
    max_x = max(p[0] for p in panels)
    min_y = min(p[1] for p in panels)
    max_y = max(p[1] for p in panels)
    for y in range(min_y, max_y + 1):
        print("".join(panels[(x, y)].label for x in range(min_x, max_x + 1)))


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
