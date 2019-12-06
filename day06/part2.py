import argparse
import sys
from typing import Dict, List, NamedTuple

import pytest


class Node(NamedTuple):
    parent: str
    name: str


def get_path_to_com(nodes: Dict[str, Node], name: str) -> List[str]:
    path = []
    while nodes[name].name != "COM":
        path.append(name)
        name = nodes[name].parent
    return path


def calc(lines: str) -> int:
    nodes: Dict[str, Node] = {}
    nodes["COM"] = Node("", "COM")

    for line in lines.strip().split("\n"):
        name_a, name_b = line.split(")")
        nodes[name_b] = Node(name_a, name_b)

    you_path = get_path_to_com(nodes, "YOU")
    san_path = get_path_to_com(nodes, "SAN")

    name_you = you_path.pop()
    name_san = san_path.pop()
    while name_you == name_san:
        name_you = you_path.pop()
        name_san = san_path.pop()

    return len(you_path) + len(san_path)


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
        ("COM)B\nB)C\nB)G\nG)YOU\nC)SAN\nG)D", 2),
        ("COM)B\nB)C\nB)G\nG)YOU\nC)SAN", 2),
        ("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN", 4),
    ),
)
def test(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
