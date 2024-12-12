from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def stone_to_ret(stone: str) -> str:
    if stone == "0":
        return "1"
    elif len(stone) % 2 == 0:
        hp = len(stone) // 2
        return str(int(stone[:hp])) + " " + str(int(stone[hp:]))
    else:
        return str(int(stone) * 2024)


def transmute_stones(stones) -> Counter:
    new_stones = Counter()
    for stone, count in stones.items():
        transformed_stones = stone_to_ret(stone).split(" ")
        for transformed_stone in transformed_stones:
            new_stones[transformed_stone] += count
    return new_stones


def count_stones(stones: list[str], iterations: int) -> int:
    stone_counter = Counter(stones)
    num_stones = 0
    for i in range(0, iterations):
        stone_counter = transmute_stones(stone_counter)
        num_stones = sum(val for val in stone_counter.values())
    return num_stones


def main(file_path: Path) -> None:
    with open(file_path.resolve(), "r") as input:
        data = input.readline()

    stones = data.split(" ")

    print(f"Part 1 with 25 iterations: {count_stones(stones, 25)}")
    print(f"Part 2 with 75 iterations: {count_stones(stones, 75)}")
    print(f"Part 3 with 5000 iterations (for science): {count_stones(stones, 5000)}")


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
