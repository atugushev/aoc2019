import argparse
import collections
import itertools
import math
import sys
from typing import Dict, List, Tuple

import pytest


def get_vaporized_asteroid(
    lines: str, station: Tuple[int, int], order_id: int
) -> Tuple[int, int]:
    matrix = tuple(tuple(line) for line in lines.strip().split("\n"))
    asteroids: Dict[
        float, List[Tuple[float, float, Tuple[int, int]]]
    ] = collections.defaultdict(list)
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value != "#":
                continue

            # Make negative degrees positive
            degree = math.degrees(math.atan2(y - station[1], x - station[0]))
            if degree < 0:
                degree += 360

            # Turn table to 90 degreees
            degree += 90
            degree %= 360

            asteroids[degree].append(
                (
                    math.sqrt((x - station[0]) ** 2 + (y - station[1]) ** 2),
                    degree,
                    (x, y),
                )
            )

    # sort in reverse order asteroids by radius
    for _, v in asteroids.items():
        v.sort(key=lambda x: -x[0])

    oid = 1
    for angle in itertools.cycle(sorted(asteroids.keys())):
        if not asteroids:
            break

        asteroid = asteroids.get(angle)
        if not asteroid:
            continue

        point = asteroid.pop()[2]
        if not asteroid:
            del asteroids[angle]

        if oid == order_id:
            return point

        oid += 1

    raise RuntimeError("Asteroid not found")


def solve(lines: str) -> int:
    point = get_vaporized_asteroid(lines, (17, 23), 200)
    return point[0] * 100 + point[1]


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


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
    "s, station, order_id, expected",
    (
        # test cases
        (map_str5, (11, 13), 100, (10, 16)),
        (map_str5, (11, 13), 200, (8, 2)),
        # ("", None),
    ),
)
def test(s: str, station: Tuple[int, int], order_id: int, expected: int) -> None:
    assert get_vaporized_asteroid(s, station, order_id) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
