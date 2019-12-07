import argparse
import sys
from collections import deque
from typing import List, Optional

import pytest
from computer import Computer


def signal(lines: str, seq: List[int]) -> int:
    seq_deq = deque(seq)
    output = 0
    computer = Computer()
    computer.read_instructions(lines)
    memory = computer.memory[:]
    while seq_deq:
        inp = seq_deq.popleft()
        computer.reset()
        computer.init_memory(memory)
        computer.stdin = deque([inp, output])
        computer.run()
        assert len(computer.stdout) == 1
        output = computer.stdout[0]

    return output


def solve(lines: str) -> Optional[int]:
    max_sig = None
    range_max = 5
    for a in range(range_max):
        for b in range(range_max):
            for c in range(range_max):
                for d in range(range_max):
                    for e in range(range_max):
                        inputs = [a, b, c, d, e]
                        if len(set(inputs)) != 5:
                            continue
                        sig = signal(lines, inputs)
                        if max_sig is None or sig > max_sig:
                            max_sig = sig
    return max_sig


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
        ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0], 43210),
        (
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
            [0, 1, 2, 3, 4],
            54321,
        ),
        (
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
            "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            [1, 0, 4, 3, 2],
            65210,
        ),
    ),
)
def test(s: str, seq: List[int], expected: int) -> None:
    assert signal(s, seq) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
