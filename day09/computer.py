import argparse
import pdb
import sys
from collections import deque
from typing import Any, Deque, List

import pytest


class Halt(Exception):
    pass


class Pause(Exception):
    pass


class Computer:
    POS_MODE = 0
    IMM_MODE = 1
    REL_MODE = 2

    def __init__(self, name: Any = None) -> None:
        self.pc = 0
        self.name = "" if name is None else name
        self.memory: List[int] = []
        self.stdout: Deque[int] = deque()
        self.stdin: Deque[int] = deque()
        self.halted = False
        self.debug = False
        self.opmode = 0
        self.relative_base = 0
        self.interactive = True

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name}) @ {self.pc}"

    def __repr__(self) -> str:
        return self.__str__()

    def reset(self) -> None:
        self.pc = 0
        self.opmode = 0
        self.memory = []
        self.stdout = deque()
        self.stdin = deque()
        self.relative_base = 0

    def init_memory(self, memory: List[int]) -> None:
        self.memory = memory + [0] * 10000

    def read_instructions(self, s: str) -> None:
        self.init_memory([int(x) for x in s.split(",")])

    def eat_memory_cell(self) -> int:
        mem_int = self.memory[self.pc]
        self.pc += 1
        return mem_int

    def eat_param(self) -> int:
        mode = self.eat_opmode()
        if mode == self.POS_MODE:
            return self.memory[self.eat_memory_cell()]
        elif mode == self.IMM_MODE:
            return self.eat_memory_cell()
        elif mode == self.REL_MODE:
            return self.memory[self.relative_base + self.eat_memory_cell()]
        else:
            raise RuntimeError(f"[{self}] unexpected mode={mode} at pc={self.pc}")

    def eat_and_store(self, value: int) -> None:
        mode = self.eat_opmode()
        if mode == self.POS_MODE:
            index = self.eat_memory_cell()
        elif mode == self.IMM_MODE:
            index = self.pc
            self.eat_memory_cell()
        elif mode == self.REL_MODE:
            index = self.relative_base + self.eat_memory_cell()
        else:
            raise RuntimeError(f"[{self}] unexpected mode={mode} at pc={self.pc}")
        self.memory[index] = value

    def eat_opmode(self) -> int:
        mode = self.opmode % 10
        self.opmode //= 10
        return mode

    def eat_opcode(self) -> int:
        opcode = self.eat_memory_cell()
        self.opmode = opcode // 100
        return opcode % 100

    def run(self) -> None:
        while True:
            opcode = self.eat_opcode()

            try:
                ophandler = getattr(self, f"opcode_{opcode}")
            except AttributeError:
                raise RuntimeError(
                    f"[{self}] Unexpected opcode={opcode} at pc={self.pc}"
                )

            try:
                ophandler()
            except (Halt, Pause):
                break

    def opcode_1(self) -> None:
        """Add"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(x + y)

    def opcode_2(self) -> None:
        """Mult"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(x * y)

    def opcode_3(self) -> None:
        """Input"""
        if self.stdin:
            x = self.stdin.popleft()
            self.log(f'[{self}] get "{x}" from stdin')
        else:
            if self.interactive:
                x = int(input("input> "))
            else:
                self.pause()
        self.eat_and_store(x)

    def opcode_4(self) -> None:
        """Print"""
        x = self.eat_param()
        self.log(f'[{self}] print "{x}" to stdout')
        self.stdout.appendleft(x)

    def opcode_5(self) -> None:
        """Jump-if-true"""
        p = self.eat_param()
        t = self.eat_param()
        if p != 0:
            self.pc = t

    def opcode_6(self) -> None:
        """Jump-if-false"""
        p = self.eat_param()
        t = self.eat_param()
        if p == 0:
            self.pc = t

    def opcode_7(self) -> None:
        """Less than"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(1 if x < y else 0)

    def opcode_8(self) -> None:
        """Equals"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(1 if x == y else 0)

    def opcode_9(self) -> None:
        """Equals"""
        self.relative_base += self.eat_param()

    def opcode_99(self) -> None:
        self.log(f"[{self}] HALTED")
        self.halted = True
        raise Halt()

    def pause(self) -> None:
        self.pc -= 1
        self.log(f"[{self}] paused")
        raise Pause()

    def log(self, s: str) -> None:
        if self.debug:
            print(s)

    def dump(self) -> None:
        values = []
        for i, v in enumerate(map(str, self.memory)):
            if self.pc == i:
                v = f"-->{i}<--"
            values.append(v)
        print(f"[{self}]", " ".join(values))


lg_str = """\
3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
"""
lg_mem = [int(x) for x in lg_str.split(",")]


@pytest.mark.parametrize(
    "memory, expected_memory, stdin, expected_stdout",
    (
        # position mode
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99], [], []),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99], [], []),
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            [],
            [],
        ),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801], [], []),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99], [], []),
        ([3, 7, 1, 7, 7, 7, 99, 0], [3, 7, 1, 7, 7, 7, 99, 20], [10], []),
        ([3, 9, 1, 9, 9, 9, 4, 9, 99, 0], [3, 9, 1, 9, 9, 9, 4, 9, 99, 20], [10], [20]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [], [0], [0]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [], [1], [1]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [], [8], [1]),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [], [88], [0]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [], [0], [1]),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [], [88], [0]),
        # immediate mode
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [], [8], [1]),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], [], [88], [0]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [], [0], [1]),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], [], [88], [0]),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [], [0], [0]),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [], [1], [1]),
        # large test
        (lg_mem, [], [7], [999]),
        (lg_mem, [], [8], [1000]),
        (lg_mem, [], [9], [1001]),
    ),
)
def test(
    memory: List[int],
    expected_memory: List[int],
    stdin: List[int],
    expected_stdout: List[int],
) -> None:
    comp = Computer()
    comp.init_memory(memory[:])
    if stdin:
        comp.stdin = deque(stdin)
    comp.run()
    if expected_memory:
        assert comp.memory == expected_memory
    if expected_stdout:
        assert comp.stdout == deque(expected_stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(sys.argv[1:])

    c = Computer()
    c.interactive = True
    c.read_instructions(args.file.read())

    try:
        c.run()
    except Exception:
        pdb.post_mortem()
        raise
    print(*c.stdout, sep="\n")
