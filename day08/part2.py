import argparse
import itertools
import sys
from typing import Any, Iterable, List

import pytest


def grouper(iterable: Iterable[Any], n: int) -> Iterable[Any]:
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def image(lines: str, x: int = 25, y: int = 6) -> str:
    size = x * y
    layers = list(grouper(lines.strip(), size))

    output = [None] * size
    for j in range(size):
        for i, _ in enumerate(layers):
            if layers[i][j] != "2":
                output[j] = layers[i][j]
                break

    return "\n".join("".join(o) for o in grouper(output, x))


def solve(lines: str) -> str:
    return image(lines, 25, 6)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


@pytest.mark.parametrize("s, expected", (("0222112222120000", "01\n10"),))
def test(s: str, expected: int) -> None:
    assert image(s, 2, 2) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
