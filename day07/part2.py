import argparse
import collections
import itertools
import sys
from typing import Generator, List, Optional, Tuple

import pytest
from computer import Computer


def signal(lines: str, seq: Tuple[int, ...]) -> int:
    seq_deq = collections.deque(seq)
    computers = []
    for i in range(5):
        comp = Computer(i)
        comp.read_instructions(lines)
        comp.stdin = collections.deque([seq_deq.popleft()])
        computers.append(comp)

    out = 0
    for comp in itertools.cycle(computers):
        comp.stdin.append(out)
        comp.run()
        out = comp.stdout.pop()

        if all(c.halted for c in computers):
            break

    return out


def all_signals(lines: str) -> Generator[int, None, None]:
    for inputs in itertools.permutations(range(5, 10)):
        yield signal(lines, inputs)


def solve(lines: str) -> Optional[int]:
    return max(all_signals(lines))


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


@pytest.mark.parametrize(
    "s, seq, expected",
    (
        (
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,"
            "4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
            (9, 8, 7, 6, 5),
            139629729,
        ),
        (
            "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
            "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
            "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
            (9, 7, 8, 5, 6),
            18216,
        ),
    ),
)
def test(s: str, seq: Tuple[int, ...], expected: int) -> None:
    assert signal(s, seq) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
