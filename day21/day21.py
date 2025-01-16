from pathlib import Path
from argparse import ArgumentParser
from itertools import pairwise
from functools import lru_cache

num_pad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["", "0", "A"]]
dir_pad = [
    ["", "^", "A"],
    ["<", "v", ">"],
]

directions = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}

numpad_lookup = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    " ": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
}

dirpad_lookup = {
    " ": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

dir_base_lookup = {
    ("A", "A"): "A",
    ("^", "^"): "A",
    (">", ">"): "A",
    ("v", "v"): "A",
    ("<", "<"): "A",
    ("A", "^"): "<A",
    ("^", "A"): ">A",
    ("A", ">"): "vA",
    (">", "A"): "^A",
    ("v", "^"): "^A",
    ("^", "v"): "vA",
    ("v", "<"): "<A",
    ("<", "v"): ">A",
    ("v", ">"): ">A",
    (">", "v"): "<A",
    ("A", "v"): "<vA",
    ("v", "A"): "^>A",
    ("A", "<"): "v<<A",
    ("<", "A"): ">>^A",
    (">", "<"): "<<A",
    ("<", ">"): ">>A",
    ("<", "^"): ">^A",
    ("^", "<"): "v<A",
    (">", "^"): "<^A",
    ("^", ">"): "v>A",
}


def pairwise_subtract(a, b):
    return (a[0] - b[0], a[1] - b[1])


def num_pad_to_dir_pad(start, goal) -> str:
    start = numpad_lookup[start]
    goal = numpad_lookup[goal]
    difference = pairwise_subtract(goal, start)
    move = ""
    if any(d == 0 for d in difference):
        if difference[0] == 0:
            move += (
                ">" * abs(difference[1])
                if difference[1] > 0
                else "<" * abs(difference[1])
            )
        elif difference[1] == 0:
            move += (
                "v" * abs(difference[0])
                if difference[0] > 0
                else "^" * abs(difference[0])
            )

    else:
        # want to move in an L shape
        horz_move = ""
        vert_move = ""
        x_dir = ""
        y_dir = ""
        if difference[1] > 0:
            amount = abs(difference[1])
            horz_move += ">" * amount
            x_dir = "RIGHT"
        else:
            amount = abs(difference[1])
            horz_move += "<" * amount
            x_dir = "LEFT"

        if difference[0] > 0:
            amount = abs(difference[0])
            vert_move += "v" * amount
            y_dir = "DOWN"
        else:
            amount = abs(difference[0])
            vert_move += "^" * amount
            y_dir = "UP"

        # because of the corner cut
        # if we are in the bottom row and going to the left column, we do y_move + x_move
        # if we are in the far left column and going to the bottom row, we do x_move + y_move
        if start[0] == 3 and goal[1] == 0:
            move += vert_move + horz_move
        elif start[1] == 0 and goal[0] == 3:
            move += horz_move + vert_move

        elif x_dir == "LEFT" and y_dir == "UP":
            move += horz_move + vert_move
        elif x_dir == "LEFT" and y_dir == "DOWN":
            move += horz_move + vert_move
        elif x_dir == "RIGHT" and y_dir == "DOWN":
            move += vert_move + horz_move
        elif x_dir == "RIGHT" and y_dir == "UP":
            move += vert_move + horz_move

    # add the required button press
    move += "A"
    return move


@lru_cache
def dir_pad_to_pad(sequence, depth=25) -> str:
    if depth == 0:
        return len(sequence)
    else:
        return sum(
            dir_pad_to_pad(dir_base_lookup[(key_start, key_end)], depth - 1)
            for key_start, key_end in pairwise(f"A{sequence}")
        )


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().splitlines()

    # For each alphanumeric character in the code, we need to compute the move to get to that character.
    # We have the starting position of the head, and the position it needs to go to. We need to see the move
    tot = 0
    for code in data:
        lsum = 0
        for key_start, key_end in pairwise(f"A{code}"):
            num_encoding = num_pad_to_dir_pad(key_start, key_end)
            dir_len = dir_pad_to_pad(num_encoding)
            lsum += dir_len

        code_int = int("".join(filter(str.isdigit, code)))
        print(f"{code_int} X {lsum}")
        tot += code_int * lsum
        print(f"Total moves: {tot}")


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
