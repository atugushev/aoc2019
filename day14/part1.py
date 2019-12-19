import argparse
import collections
import dataclasses
import math
import sys
from typing import List, Tuple

import pytest


@dataclasses.dataclass(frozen=True)
class Chemical:
    name: str
    qty: int

    @classmethod
    def from_string(cls, s: str) -> "Chemical":
        qty, name = s.strip().split(" ")
        return cls(name.strip(), int(qty.strip()))

    @classmethod
    def from_string_comma_list(cls, s: str) -> Tuple["Chemical", ...]:
        return tuple(cls.from_string(c) for c in s.split(","))

    def __add__(self, other: int):
        assert self.name == other.name
        return type(self)(name=self.name, qty=self.qty + other.qty)


def search(inputs, chemicals, node, outputs_qty, mult):
    for child in chemicals[node]:
        if child.name in inputs:
            outputs_qty[child.name] += child.qty * mult
        else:
            search(inputs, chemicals, child.name, outputs_qty, mult * child.qty)


def solve(lines: str) -> int:
    chemicals: Dict[str, Tuple[Chemical, ...]] = {}
    inputs: Dict[str, Tuple[Chemical, ...]] = {}
    for line in lines.strip().split("\n"):
        in_, out = line.split("=>")
        in_chem = Chemical.from_string(out)
        chemicals[in_chem.name] = [
            Chemical(c.name, c.qty) for c in Chemical.from_string_comma_list(in_)
        ]

        if chemicals[in_chem.name][0].name == "ORE":
            assert len(chemicals[in_chem.name]) == 1
            inputs[in_chem.name] = [in_chem, chemicals[in_chem.name][0]]

    print(chemicals)

    outputs_qty = collections.defaultdict(int)
    breakpoint()
    search(inputs, chemicals, "FUEL", outputs_qty, 1)
    print("in", inputs)
    print("out", outputs_qty)

    return sum(
        math.ceil(qty / inputs[name][0].qty) * inputs[name][1].qty
        for name, qty in outputs_qty.items()
    )


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


reactions1 = """\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 2 E
1 E, 7 A => 1 FUEL
"""

reactions2 = """\
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

reactions3 = """\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""


@pytest.mark.parametrize(
    "s, expected",
    (
        # test cases
        (reactions1, 31),
        (reactions2, 165),
        (reactions3, 13312),
        # ("", None),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
