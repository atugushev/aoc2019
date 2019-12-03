import argparse
import sys
from typing import Dict, List, NamedTuple, Optional

import pytest


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, point: "Point") -> "Point":  # type: ignore
        return Point(self.x + point.x, self.y + point.y)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def dist(self, other: "Optional[Point]" = None) -> int:
        if other is None:
            other = Point(0, 0)

        return abs(self.x - other.x) + abs(self.y - other.y)


def get_points(path: List[str]) -> Dict[Point, int]:
    points = {}
    curr_point = Point(0, 0)
    steps = 0
    for move in path:
        direction = move[:1]
        distance = int(move[1:])
        for _ in range(distance):
            if direction == "U":  # [0, 1]
                curr_point += Point(0, 1)
            elif direction == "D":  # [0, -1]
                curr_point += Point(0, -1)
            elif direction == "L":  # [-1, 0]
                curr_point += Point(-1, 0)
            elif direction == "R":  # [0, 1]
                curr_point += Point(1, 0)
            steps += 1
            points[curr_point] = steps
    return points


def get_shortest_steps(points1: Dict[Point, int], points2: Dict[Point, int]) -> int:
    intersection = set(points1.keys()) & set(points2.keys())
    return min((points1[p] + points2[p], p.dist()) for p in intersection)[0]


def calc(data: str) -> int:
    path1_str, path2_str = data.split("\n")
    path1 = path1_str.strip().split(",")
    path2 = path2_str.strip().split(",")

    points1 = get_points(path1)
    points2 = get_points(path2)

    return get_shortest_steps(points1, points2)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)

    print(calc(args.infile.read()))

    return 0


@pytest.mark.parametrize(
    "s, expected",
    (
        ("R8,U5,L5,D3\nU7,R6,D4,L4", 30),
        ("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83", 610),
    ),
)
def test_calc(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
