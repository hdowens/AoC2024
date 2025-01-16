from pathlib import Path
from argparse import ArgumentParser
import re


def pprint_eq(a_vals, b_vals, prize) -> None:
    print(f"{a_vals[0]}A + {b_vals[0]}B = {prize[0]}")
    print(f"{a_vals[1]}A + {b_vals[1]}B = {prize[1]}")


def cramer_rule(a_vals, b_vals, prize) -> int:
    det = (a_vals[0] * b_vals[1]) - (a_vals[1] * b_vals[0])
    det_a = (prize[0] * b_vals[1]) - (prize[1] * b_vals[0])
    det_b = (a_vals[0] * prize[1]) - (a_vals[1] * prize[0])
    a = det_a / det
    b = det_b / det
    if a.is_integer() and b.is_integer():
        return int(a), int(b)


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().split("\n\n")

    total_tickets = 0
    total_tickets_p2 = 0
    for game in data:
        instructions = game.split("\n")
        a_vals = list(map(int, (re.findall(r"(\d+)", instructions[0]))))
        b_vals = list(map(int, (re.findall(r"(\d+)", instructions[1]))))
        prize = list(map(int, (re.findall(r"(\d+)", instructions[2]))))

        vals = cramer_rule(a_vals, b_vals, prize)
        if vals:
            # print(3*vals[0] + vals[1])
            total_tickets += 3 * vals[0] + vals[1]

        # part2
        prize[0] = prize[0] + 10000000000000
        prize[1] = prize[1] + 10000000000000
        p2_vals = cramer_rule(a_vals, b_vals, prize)
        if p2_vals:
            total_tickets_p2 += 3 * p2_vals[0] + p2_vals[1]

    print(total_tickets)
    print(total_tickets_p2)


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
