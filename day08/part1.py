import argparse
import collections
import itertools
import sys
from typing import Any, Generator, Iterable, List, Tuple


def grouper(iterable: Iterable[Any], n: int) -> Iterable[Any]:
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def zero_count_per_layer(lines: str) -> Generator[Tuple[int, str], None, None]:
    for layer in grouper(lines.strip(), 25 * 6):
        yield collections.Counter(layer)["0"], layer


def solve(lines: str) -> int:
    layer = min(zero_count_per_layer(lines), key=lambda x: x[0])[1]
    counter = collections.Counter(layer)
    return counter["1"] * counter["2"]


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args(argv)
    print(solve(args.infile.read()))
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
