import argparse
import os
import sys
import time
from enum import IntEnum
from typing import Dict, List, Tuple

import pytest

from computer import Computer


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    @property
    def label(self):
        # return "·█▓_●"[self.value]
        return " █▓_●"[self.value]


def solve(lines: str) -> int:
    comp = Computer()
    # comp.debug = True

    score = None
    comp.read_instructions(lines)
    comp.memory[0] = 2
    grid = {}

    """
    def stdout_handler(x):
        print("my", x)
    comp.stdout_handler = stdout_handler
    """

    padddle_x = 0
    ball_x = 0

    tick = 0

    def stdin_handler():
        nonlocal score
        nonlocal grid
        nonlocal padddle_x
        nonlocal ball_x
        nonlocal tick
        tick += 1
        while comp.stdout:
            value = comp.stdout.pop()
            y = comp.stdout.pop()
            x = comp.stdout.pop()
            if x == -1 and y == 0:
                score = value
            else:
                t = Tile(value)
                point = (x, y)
                grid[point] = t
                if t == Tile.PADDLE:
                    padddle_x = x
                if t == Tile.BALL:
                    ball_x = x
        if tick % 20 == 0:
            draw(grid, score)
        if padddle_x > ball_x:
            v = -1
        elif padddle_x < ball_x:
            v = 1
        else:
            v = 0
        comp.stdin.append(v)
        if tick % 20 == 0:
            time.sleep(0.05)

    comp.stdin_handler = stdin_handler

    comp.run()
    stdin_handler()
    draw(grid, score)
    print("tick", tick)
    return score


def draw(panels: Dict[Tuple[int, int], int], score) -> None:
    min_x = min(p[0] for p in panels)
    max_x = max(p[0] for p in panels)
    min_y = min(p[1] for p in panels)
    max_y = max(p[1] for p in panels)
    os.system("clear")
    print(" " * 3 + "".join(str(x // 10) for x in range(min_x, max_x + 1)))
    print(" " * 3 + "".join(str(x % 10) for x in range(min_x, max_x + 1)))
    for y in range(min_y, max_y + 1):
        print(
            f"{y:2d} "
            + "".join(
                panels.get((x, y), Tile(0)).label for x in range(min_x, max_x + 1)
            )
        )
    print("{0:^{1}}".format(f"SCORE: {score}", max_x))


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    try:
        print(solve(args.infile.read()))
    except Exception:
        import pdb

        pdb.post_mortem()
        raise

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
