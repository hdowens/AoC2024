from pathlib import Path
from argparse import ArgumentParser
from functools import cache


@cache
def recursive_search(towel, patterns):
    if towel == "":
        return 1
    return sum(
        recursive_search(towel.removeprefix(p), patterns)
        for p in patterns
        if towel.startswith(p)
    )


@cache
def recursive_len(towel, patterns):
    if towel == "":
        return False
    return any(
        recursive_search(towel.removeprefix(p), patterns)
        for p in patterns
        if towel.startswith(p)
    )


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().strip().split("\n\n")

    patterns, data = tuple(data[0].split(", ")), data[1].splitlines()

    print(f"Part 1: {sum(recursive_len(towel, patterns) for towel in data)}")
    print(f"Part 2: {sum(recursive_search(towel, patterns) for towel in data)}")


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t", "--test", action="store_true", help="Read from test_input.txt"
    )
    group.add_argument(
        "-p", "--puzzle", action="store_true", help="Read from puz_input.txt"
    )

    args = parser.parse_args()

    if args.test:
        file_path = Path("test_input.txt")
    elif args.puzzle:
        file_path = Path("puz_input.txt")

    main(file_path)
