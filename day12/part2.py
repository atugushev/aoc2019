import argparse
import itertools
import math
import pdb
import re
import sys
from dataclasses import astuple, dataclass, fields
from typing import Dict, List, Tuple

import pytest


@dataclass
class Vec:
    x: int
    y: int
    z: int

    @classmethod
    def axis_names(cls) -> Tuple[str, ...]:
        return tuple(f.name for f in fields(cls))

    def __add__(self, other: "Vec") -> "Vec":
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec") -> "Vec":
        return type(self)(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other: "Vec") -> "Vec":
        for axis in self.axis_names():
            self[axis] += other[axis]
        return self

    def __isub__(self, other: "Vec") -> "Vec":
        for axis in self.axis_names():
            self[axis] -= other[axis]
        return self

    def __getitem__(self, name: str) -> int:
        return getattr(self, name)

    def __setitem__(self, name: str, value: int) -> None:
        setattr(self, name, value)

    def compare(self, other: "Vec") -> "Vec":
        kwargs = {}
        for axis in self.axis_names():
            kwargs[axis] = int(self[axis] < other[axis]) - int(self[axis] > other[axis])
        return type(self)(**kwargs)


@dataclass
class Moon:
    pos: Vec
    vel: Vec

    REPR_RE = re.compile(r"=(-?\d+)")

    @property
    def pot(self) -> int:
        return sum(map(abs, astuple(self.pos)))

    @property
    def kin(self) -> int:
        return sum(map(abs, astuple(self.vel)))

    @classmethod
    def from_string(cls, s: str) -> "Moon":
        return cls(pos=Vec(*map(int, cls.REPR_RE.findall(s))), vel=Vec(0, 0, 0))


def compute_period(lines: str) -> int:
    orig_moons = [Moon.from_string(line) for line in lines.strip().split("\n")]
    moons = orig_moons[:]

    axes_periods: Dict[str, int] = {}
    orig_moons_axes = {axis: get_axes(orig_moons, axis) for axis in Vec.axis_names()}

    step = 0
    while len(axes_periods) < 3:
        step += 1

        for moon1, moon2 in itertools.combinations(moons, 2):
            vec = moon1.pos.compare(moon2.pos)
            moon1.vel += vec
            moon2.vel -= vec

        for moon in moons:
            moon.pos += moon.vel

        for axis in Vec.axis_names():
            if axis in axes_periods:
                continue

            moons_axes = get_axes(moons, axis)
            if moons_axes == orig_moons_axes[axis]:
                axes_periods[axis] = step

    return lcm(*axes_periods.values())


def get_axes(moons: List[Moon], axis: str) -> Tuple[Tuple[int, int], ...]:
    return tuple((moon.pos[axis], moon.vel[axis]) for moon in moons)


def lcm(*args: int) -> int:
    a = args[0]
    for b in args[1:]:
        a = (a * b) // math.gcd(a, b)
    return a


def solve(lines: str) -> int:
    try:
        return compute_period(lines)
    except Exception:
        pdb.post_mortem()
        raise


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


scan1 = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

scan2 = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""


@pytest.mark.parametrize(
    "s, expected",
    (
        # test cases
        (scan1, 2772),
        (scan2, 4686774924),
    ),
)
def test(s: str, expected: int) -> None:
    assert compute_period(s) == expected


if __name__ == "__main__":
    main(sys.argv[1:])
