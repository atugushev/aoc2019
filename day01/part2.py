import argparse
import sys
from typing import List

import pytest


def calc(lines: str) -> int:
    def calc_fuel(m: int) -> int:
        return max(m // 3 - 2, 0)

    total = 0
    for mass in lines.splitlines():
        fuel = calc_fuel(int(mass))
        while fuel > 0:
            total += fuel
            fuel = calc_fuel(fuel)

    return total


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(calc(args.infile.read()))
    return 0


@pytest.mark.parametrize("s, expected", (("14", 2), ("1969", 966), ("100756", 50346)))
def test(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
