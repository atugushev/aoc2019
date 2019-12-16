import argparse
import pdb
import sys
from collections import deque
from typing import Any, Deque, List


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
        return f"{self.__class__.__name__}({self.name}) @ {self.pc:03d}"

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
        self.memory = memory + [0] * 1000

    def read_instructions(self, s: str) -> None:
        self.init_memory([int(x) for x in s.split(",")])

    def eat_memory_cell(self) -> int:
        mem_int = self.memory[self.pc]
        self.pc += 1
        return mem_int

    def eat_param(self) -> int:
        mode = self.eat_opmode()
        if mode == self.POS_MODE:
            param = self.memory[self.eat_memory_cell()]
        elif mode == self.IMM_MODE:
            param = self.eat_memory_cell()
        elif mode == self.REL_MODE:
            param = self.memory[self.relative_base + self.eat_memory_cell()]
        else:
            raise RuntimeError(f"[{self}] unexpected mode={mode} at pc={self.pc}")

        self.log(f" {param}", end="")
        return param

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
        self.log(f" {value}", end="")
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
            self.log(f"[{self}] ", end="")
            opcode = self.eat_opcode()

            try:
                ophandler = getattr(self, f"opcode_{opcode}")
            except AttributeError:
                raise RuntimeError(
                    f"[{self}] Unexpected opcode={opcode} at pc={self.pc}"
                )

            self.log(ophandler.__doc__, end="")
            try:
                ophandler()
            except (Halt, Pause):
                break
            finally:
                self.log("")

    def opcode_1(self) -> None:
        """add"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(x + y)

    def opcode_2(self) -> None:
        """mult"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(x * y)

    def opcode_3(self) -> None:
        """input"""
        if self.stdin:
            x = self.stdin.popleft()
        else:
            if self.interactive:
                self.log("\nIntCode is awaiting an input ...")
                x = int(input("input> "))
            else:
                self.pause()
        self.eat_and_store(x)

    def opcode_4(self) -> None:
        """print"""
        x = self.eat_param()
        self.stdout.appendleft(x)

    def opcode_5(self) -> None:
        """jump-if-true"""
        p = self.eat_param()
        t = self.eat_param()
        if p != 0:
            self.pc = t

    def opcode_6(self) -> None:
        """jump-if-false"""
        p = self.eat_param()
        t = self.eat_param()
        if p == 0:
            self.pc = t

    def opcode_7(self) -> None:
        """less-than"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(1 if x < y else 0)

    def opcode_8(self) -> None:
        """equals"""
        x = self.eat_param()
        y = self.eat_param()
        self.eat_and_store(1 if x == y else 0)

    def opcode_9(self) -> None:
        """adj-rel-base"""
        self.relative_base += self.eat_param()

    def opcode_99(self) -> None:
        """halt"""
        self.halted = True
        raise Halt()

    def pause(self) -> None:
        self.pc -= 1
        raise Pause()

    def log(self, s: str, end: str = "\n") -> None:
        if self.debug:
            print(s, end=end)

    def dump(self) -> None:
        values = []
        for i, v in enumerate(map(str, self.memory)):
            if self.pc == i:
                v = f"-->{i}<--"
            values.append(v)
        print(f"[{self}]", " ".join(values))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parser.add_argument("--stdin", type=str, action="append")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(sys.argv[1:])

    c = Computer()
    c.debug = args.debug
    c.interactive = True
    if args.stdin:
        c.stdin = deque(map(int, args.stdin))
    c.read_instructions(args.file.read())

    try:
        c.run()
    except Exception:
        pdb.post_mortem()
        raise
    print(*c.stdout, sep="\n")
