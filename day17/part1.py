import pdb
import argparse
import sys
from typing import List
from computer import Computer
from pprint import pprint

import pytest

TILES = {35: "#", 46: ".", 10: "\n"}
CODES = {v: k for k, v in TILES.items()}

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def solve(lines: str) -> int:
    comp = Computer()
    comp.read_instructions(lines)
    comp.run()

    grid = {}

    x, y = 0, 0
    for code in comp.stdout:
        print(TILES.get(code, chr(code)), end='')

        p = (x, y)
        grid[p] = code

        x += 1
        if code == 10:
            x = 0
            y += 1

    return compute(grid)

def compute(grid):
    res = []
    for p in grid:
        if grid[p] != 35:
            continue
        try:
            for d in DIRS:
                if grid[(p[0]+d[0], p[1]+d[1])] != 35:
                    raise RuntimeError("not good")
        except (KeyError, RuntimeError):
            pass
        else:
            res.append(p)

    print(len(res))
    pprint(res)
    return sum(p[0] * p[1] for p in res)


def parse_grid_str(s):
    grid = {}
    x, y = 0, 0
    for y, line in enumerate(s.strip().split('\n')):
        for x, value in enumerate(line):
            grid[(x, y)] = CODES.get(value, ord(value))
    return grid

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    try:
        print(solve(args.infile.read().strip()))
    except Exception:
        pdb.post_mortem()
        raise
    return 0


grid1="""\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
"""

@pytest.mark.parametrize(
    "s, expected",
    (
        # test cases
        # ("", None),
        (grid1, 76),
    ),
)
def test(s: str, expected: int) -> None:
    grid = parse_grid_str(s)
    assert compute(grid) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
