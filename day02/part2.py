import argparse
import sys
from typing import List

import pytest


def calc_first_elem(memory: List[int]) -> int:
    i = 0
    while i < len(memory):
        opcode = memory[i]
        if opcode == 1:
            memory[memory[i + 3]] = memory[memory[i + 1]] + memory[memory[i + 2]]
        elif opcode == 2:
            memory[memory[i + 3]] = memory[memory[i + 1]] * memory[memory[i + 2]]
        elif opcode == 99:
            break
        else:
            raise Exception(f"Unhandled opcode={opcode} at i={i}")
        i += 4
    return memory[0]


def calc(opcodes: str) -> int:
    memory = [int(x) for x in opcodes.split(",")]
    for noun in range(100):
        for verb in range(100):
            memory_temp = memory[:]
            memory_temp[1] = noun
            memory_temp[2] = verb
            output = calc_first_elem(memory_temp)
            if output == 19690720:
                return 100 * noun + verb
    return -1


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)

    print(calc(args.infile.read()))

    return 0


@pytest.mark.parametrize(
    "memory, expected",
    (
        ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], 3500),
        ([1, 0, 0, 0, 99], 2),
        ([2, 3, 0, 3, 99], 2),
        ([2, 4, 4, 5, 99, 0], 2),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], 30),
    ),
)
def test(memory: List[int], expected: int) -> None:
    assert calc_first_elem(memory) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
