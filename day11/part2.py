import argparse
import collections
import sys
from typing import Dict, List, Tuple

from computer import Computer


def solve(lines: str) -> None:
    c = Computer()
    c.interactive = False
    c.read_instructions(lines)

    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # Right Down Left Up
    panels: Dict[Tuple[int, int], int] = collections.defaultdict(int)

    point = (0, 0)
    panels[point] = 1  # Part2
    angle = 90  # Starting angle
    while not c.halted:
        c.stdin.append(panels[point])
        c.run()

        color_out = c.stdout.pop()
        direction_out = c.stdout.pop()
        panels[point] = color_out

        angle += 90 * (1 - 2 * direction_out)
        direction = angle // 90 % 4
        point = (
            point[0] + directions[direction][0],
            point[1] + directions[direction][1],
        )

    draw(panels)


def draw(panels: Dict[Tuple[int, int], int]) -> None:
    min_x = min(p[0] for p in panels)
    max_x = max(p[0] for p in panels)
    min_y = min(p[1] for p in panels)
    max_y = max(p[1] for p in panels)
    for y in range(min_y, max_y + 1):
        print("".join("·█"[panels[(x, y)]] for x in range(min_x, max_x + 1)))


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    solve(args.infile.read())
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
