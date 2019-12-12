import argparse
import collections
import sys
from typing import Dict, List, Set, Tuple

from computer import Computer


def solve(lines: str) -> int:
    c = Computer()
    c.interactive = False
    c.read_instructions(lines)

    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # Right Down Left Up
    panels: Dict[Tuple[int, int], int] = collections.defaultdict(int)
    painted_panels: Set[Tuple[int, int]] = set()

    point = (0, 0)
    painted_panels.add(point)
    angle = 90  # Starting angle
    while not c.halted:
        c.stdin.append(panels[point])
        c.run()

        color_out = c.stdout.pop()
        direction_out = c.stdout.pop()
        panels[point] = color_out
        painted_panels.add(point)

        angle += 90 * (1 - 2 * direction_out)
        direction = angle // 90 % 4
        point = (
            point[0] + directions[direction][0],
            point[1] + directions[direction][1],
        )

    return len(painted_panels)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
