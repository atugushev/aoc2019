import argparse
import sys
from typing import List

import pytest


def calc(lines: str) -> int:
    return sum(int(mass) // 3 - 2 for mass in lines.splitlines())


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)

    print(calc(args.infile.read()))

    return 0


@pytest.mark.parametrize(
    "s, expected", (("12", 2), ("14", 2), ("1969", 654), ("100756", 33583))
)
def test(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
