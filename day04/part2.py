import argparse
import sys
from typing import List

import pytest


def possible_password(num: int) -> int:
    return has_exclusive_double(num) and never_decrease(num)


def has_exclusive_double(n: int) -> bool:
    n_str = str(n)
    stack = [n_str[0]]
    for d in n_str[1:]:
        if d == stack[0]:
            stack.append(d)
        else:
            if len(stack) == 2:
                return True
            else:
                stack = [d]
    return len(stack) == 2


def never_decrease(n: int) -> bool:
    n_str = str(n)
    prev = n_str[0]
    for d in n_str[1:]:
        if d < prev:
            return False
        prev = d
    return True


def calc(lines: str) -> int:
    a, b = [int(x) for x in lines.split("-")]
    res = 0
    for num in range(a, b + 1):
        if possible_password(num):
            res += 1
    return res


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)

    print(calc(args.infile.read()))

    return 0


@pytest.mark.parametrize(
    "n, expected",
    ((123456, False), (1233555, True), (12341, False), (4321, False), (123444, False)),
)
def test_has_double(n: int, expected: int) -> None:
    assert has_exclusive_double(n) is expected


@pytest.mark.parametrize(
    "n, expected",
    ((1233555, True), (123456, True), (1123456, True), (12341, False), (123454, False)),
)
def test_never_decrease(n: int, expected: int) -> None:
    assert never_decrease(n) is expected


@pytest.mark.parametrize(
    "n, expected", ((112233, True), (123444, False), (111122, True))
)
def test_possible_password(n: int, expected: int) -> None:
    assert possible_password(n) is expected


if __name__ == "__main__":
    main(sys.argv[1:])
