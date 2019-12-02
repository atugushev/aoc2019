import argparse
import sys
from typing import List

import pytest


def calc(memory_str: str) -> str:
    memory = [int(x) for x in memory_str.split(",")]
    i = 0
    while i < len(memory):
        code = memory[i]
        if code == 1:
            memory[memory[i + 3]] = memory[memory[i + 1]] + memory[memory[i + 2]]
            i += 4
        elif code == 2:
            memory[memory[i + 3]] = memory[memory[i + 1]] * memory[memory[i + 2]]
            i += 4
        elif code == 99:
            break
        else:
            i += 1
    return ",".join(str(x) for x in memory)


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
        ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
        ("1,0,0,0,99", "2,0,0,0,99"),
        ("2,3,0,3,99", "2,3,0,6,99"),
        ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
        ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
    ),
)
def test(s: str, expected: int) -> None:
    assert calc(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
