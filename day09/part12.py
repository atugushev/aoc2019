import argparse
import sys
from typing import List

import pytest

from computer import Computer


def solve(lines: str) -> List[int]:
    computer = Computer()
    computer.read_instructions(lines)
    computer.run()
    return list(computer.stdout)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


@pytest.mark.parametrize(
    "s, expected",
    (
        (
            "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
            list(
                reversed(
                    [
                        109,
                        1,
                        204,
                        -1,
                        1001,
                        100,
                        1,
                        100,
                        1008,
                        100,
                        16,
                        101,
                        1006,
                        101,
                        0,
                        99,
                    ]
                )
            ),
        ),
        ("104,1125899906842624,99", [1125899906842624]),
        ("1102,34915192,34915192,7,4,7,99,0", [1219070632396864]),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
