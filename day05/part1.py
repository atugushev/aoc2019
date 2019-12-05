import argparse
import sys
from typing import List, Optional, Tuple

import pytest

POSITION_MODE = 0
IMMEDIATE_MODE = 1


def int_to_list_digits(i: int) -> List[int]:
    parts = list(reversed(list(str(i))))
    parts_length = len(parts)
    if parts_length < 3:
        parts += ["0"] * (3 - parts_length)
    return [int(x) for x in parts]


def get_mode_and_opcode(num: int) -> Tuple[Optional[List[int]], int]:
    return (int_to_list_digits(num // 100), num % 100) if num >= 100 else (None, num)


def get_address(
    memory: List[int], i: int, shift: int, mode: Optional[List[int]]
) -> int:
    mode_i = shift - 1
    if mode is None or mode[mode_i] == POSITION_MODE:
        return memory[i + shift]
    elif mode[mode_i] == IMMEDIATE_MODE:
        return i + shift
    else:
        raise AssertionError(f"Unknown mode: {mode[mode_i]}")


def process(memory: List[int], inp: Optional[int] = None) -> List[int]:
    output = []
    i = 0
    while i < len(memory):
        mode, opcode = get_mode_and_opcode(memory[i])
        if opcode == 1:
            memory[get_address(memory, i, 3, mode)] = (
                memory[get_address(memory, i, 1, mode)]
                + memory[get_address(memory, i, 2, mode)]
            )
            i += 4
        elif opcode == 2:
            memory[get_address(memory, i, 3, mode)] = (
                memory[get_address(memory, i, 1, mode)]
                * memory[get_address(memory, i, 2, mode)]
            )
            i += 4
        elif opcode == 3:
            value = inp or int(input("Enter input value: "))
            memory[get_address(memory, i, 1, mode)] = value
            i += 2
        elif opcode == 4:
            output.append(memory[get_address(memory, i, 1, mode)])
            i += 2
        elif opcode == 99:
            break
        else:
            raise Exception(
                f"Unhandled opcode={opcode} at i={i}. Current memory cell: {memory[i]}."
            )
    return output


def calc(opcodes: str) -> str:
    memory = [int(x) for x in opcodes.split(",")]
    for line in process(memory):
        print(line)
    return "OK"


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
        ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], []),
        ([1, 0, 0, 0, 99], []),
        ([1101, 10, 20, 0, 4, 0, 99], [30]),
        ([2, 3, 0, 3, 99], []),
        ([2, 4, 4, 5, 99, 0], []),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], []),
    ),
)
def test(memory: List[int], expected: int) -> None:
    assert process(memory, inp=2) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
