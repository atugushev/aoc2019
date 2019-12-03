import argparse
import sys
from typing import List, NamedTuple, Optional, Set

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


def get_points(path: List[str]) -> Set[Point]:
    points = set()
    curr_point = Point(0, 0)
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
            points.add(curr_point)
    return points


def get_shortest_distance(points: Set[Point]) -> int:
    return min(p.dist() for p in points)


def calc(data: str) -> int:
    path1_str, path2_str = data.split("\n")
    path1 = path1_str.strip().split(",")
    path2 = path2_str.strip().split(",")

    points1 = get_points(path1)
    points2 = get_points(path2)

    return get_shortest_distance(points1 & points2)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)

    print(calc(args.infile.read()))

    return 0


def test_point() -> None:
    assert str(Point(1, 1)) == "Point(1, 1)"
    assert Point(1, 2) + Point(4, 8) == Point(5, 10)

    x = Point(1, 2)
    x += Point(3, 4)
    assert x == Point(4, 6)


@pytest.mark.parametrize(
    "path, expected",
    (
        (["R1", "U1"], {Point(1, 0), Point(1, 1)}),
        (
            ["R1", "U1", "L2", "D2"],
            {
                Point(-1, -1),
                Point(-1, 0),
                Point(-1, 1),
                Point(0, 1),
                Point(1, 0),
                Point(1, 1),
            },
        ),
    ),
)
def test_get_points(path: List[str], expected: Set[Point]) -> None:
    assert get_points(path) == expected


@pytest.mark.parametrize(
    "points, expected",
    (
        ({Point(-1, -1), Point(2, 2), Point(3, 3)}, 2),
        ({Point(1, 2), Point(2, 1), Point(2, 2), Point(3, 3)}, 3),
    ),
)
def test_get_shortest_dist(points: Set[Point], expected: Point) -> None:
    assert get_shortest_distance(points) == expected


@pytest.mark.parametrize("s, expected", (("R8,U5,L5,D3\nU7,R6,D4,L4", 6),))
def test_calc(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
