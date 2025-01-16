from pathlib import Path
from argparse import ArgumentParser


def schematic_to_height(schematic: list) -> list:
    transposed_schematic = list(map(list, zip(*schematic)))
    return [i.count("#") - 1 for i in transposed_schematic]


# this is very crude due to hardcoding lock length
def match(lock_list: list, key_list: list) -> bool:
    return all(lock + key <= 5 for lock, key in zip(lock_list, key_list))


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        schematics = file.read().split("\n\n")

    locks = []
    keys = []
    for s in schematics:
        lines = s.split("\n")
        if all("#" in line for line in lines[0]):
            locks.append(lines)
        if all("#" in line for line in lines[-1]):
            keys.append(lines)

    lock_heights = [schematic_to_height(lock) for lock in locks]
    key_heights = [schematic_to_height(key) for key in keys]

    count = 0
    for lock in lock_heights:
        for key in key_heights:
            if match(lock, key):
                count += 1

    print(count)


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
