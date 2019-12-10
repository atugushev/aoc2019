import argparse
import collections
import math
import sys
from typing import Dict, List, Set, Tuple

import pytest


def solve(lines: str) -> int:
    matrix = tuple(tuple(line) for line in lines.strip().split("\n"))
    points = set()
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            point = (x, y)
            if value == "#":
                points.add(point)

    stat: Dict[Tuple[int, int], Set[float]] = collections.defaultdict(set)
    for x, y in points:
        point = (x, y)
        for i, j in points - {(x, y)}:
            stat[point].add(math.atan2(j - y, i - x))
    found_point = max(stat.keys(), key=lambda x: len(stat[x]))
    print(f"found point: {found_point}")
    return len(stat[found_point])


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


map_str = """\
.#..#
.....
#####
....#
...##
"""

map_str2 = """\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

map_str3 = """\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""


map_str4 = """\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""


map_str5 = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""


@pytest.mark.parametrize(
    "s, expected",
    (
        # test cases
        (map_str, 8),
        (map_str2, 33),
        (map_str3, 35),
        (map_str4, 41),
        (map_str5, 210),
        # ("", None),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
