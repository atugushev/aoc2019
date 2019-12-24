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

    def __add__(self, other: int):
        assert self.name == other.name
        return type(self)(name=self.name, qty=self.qty + other.qty)

@dataclasses.dataclass(frozen=True)
class Reaction:
    name: str
    qty: int
    chemicals: List[Chemical]

    @classmethod
    def from_string(cls, s: str) -> "Reaction":
        in_, out = s.split("=>")
        in_chem = Chemical.from_string(out)
        return cls(
            name=in_chem.name,
            qty=in_chem.qty,
            chemicals = tuple(Chemical.from_string(c) for c in in_.split(",")),
        )


def search(inputs, reactions, node, outputs_qty, mult):
    for child in reactions[node].chemicals:
        if child.name in inputs:
            outputs_qty[child.name] += child.qty * math.ceil(mult / reactions[node].qty)
        else:
            search(inputs, reactions, child.name, outputs_qty, mult * child.qty)


def solve(lines: str) -> int:
    reactions: Dict[str, Tuple[Chemical, ...]] = {}
    inputs: Dict[str, Tuple[Chemical, ...]] = {}
    for line in lines.strip().split("\n"):
        reaction = Reaction.from_string(line)
        reactions[reaction.name] = reaction

        if reaction.chemicals[0].name == "ORE":
            assert len(reaction.chemicals) == 1
            inputs[reaction.name] = reaction

    print(reactions)
    print(inputs)


    outputs_qty = collections.defaultdict(int)
    search(inputs, reactions, "FUEL", outputs_qty, 1)
    print("in", inputs)
    print("out", outputs_qty)

    return sum(
        math.ceil(qty / inputs[name].qty) * inputs[name].chemicals[0].qty
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


r1 = """\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
1 E, 7 A => 1 FUEL
"""

r2 = """\
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

r3 = """\
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

r4 = """\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""



@pytest.mark.parametrize(
    "s, expected",
    (
        # test cases
        (r1, 31),
        (r2, 165),
        (r3, 13312),
        (r4, 180697),
    ),
)
def test(s: str, expected: int) -> None:
    assert solve(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
