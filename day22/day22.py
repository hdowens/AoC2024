from pathlib import Path
from argparse import ArgumentParser
from functools import lru_cache
from collections import defaultdict


def mix_and_prune(original, new) -> int:
    return (original ^ new) & (16777216 - 1)


@lru_cache(maxsize=None)
def next_secret(secret: int) -> int:
    # step 1
    secret = mix_and_prune(secret << 6, secret)
    secret = mix_and_prune(secret >> 5, secret)
    secret = mix_and_prune(secret << 11, secret)
    return secret


def part1(data: list) -> None:
    secret_nums = list(map(int, data))
    tot = 0
    for secret in secret_nums:
        for i in range(2000):
            secret = next_secret(secret)
        # print(secret)
        tot += secret
    print(f"Part 1: {tot}")


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().splitlines()
    part1(data)

    secret_nums = list(map(int, data))
    total_nanners = defaultdict(int)
    for secret in secret_nums:
        seen = set()
        price_changes = []
        prev = secret % 10
        for i in range(2000):
            secret = next_secret(secret)
            last_digit = secret % 10
            price_changes.append(last_digit - prev)
            prev = last_digit

            if i >= 3:
                seq = tuple(price_changes[-4:])
                if seq not in seen:
                    total_nanners[seq] += last_digit
                    seen.add(seq)

    print(f"Part 2: {max(total_nanners.values())}")


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
