from pathlib import Path
from argparse import ArgumentParser

directions = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def print_grid(grid, width, height):
    for x in range(width):
        row = ""
        for y in range(height):
            row += grid[(x, y)]
        print(row)
    print()


def p1_parse_input(data: str) -> list:
    grid, moves = data.split("\n\n")

    grid_dict = {}
    for x, row in enumerate(grid.split("\n")):
        for y, cell in enumerate(row):
            if cell == "@":
                start = (x, y)
            grid_dict[(x, y)] = cell

    moves = moves.replace("\n", "")

    return grid_dict, start, moves


def sum_box_coords(grid, char):
    total = 0
    for key, val in grid.items():
        if val == char:
            total += (100 * key[0]) + key[1]
    return total


def part1(data):
    grid, start, moves = p1_parse_input(data)
    x, y = start
    for move in moves:
        dx, dy = directions[move]
        next_pos = (x + dx, y + dy)

        if grid[next_pos] == "#":
            continue

        elif grid[next_pos] == ".":
            grid[(x, y)] = "."
            grid[next_pos] = "@"
            x, y = next_pos

        elif grid[next_pos] == "O":
            # here we want to move the robot to the position of the O
            # and we want to move the O to the next available '.' position
            # we also want to update the grid dictionary
            next_o_pos = next_pos
            while grid[next_o_pos] != ".":
                if grid[next_o_pos] == "#":
                    next_o_pos = (-1, -1)
                    break
                next_o_pos = (next_o_pos[0] + dx, next_o_pos[1] + dy)

            if next_o_pos[0] != -1 and next_o_pos[1] != -1:
                grid[next_o_pos] = "O"
                grid[next_pos] = "@"
                grid[(x, y)] = "."
                x, y = next_pos

    return sum_box_coords(grid, "O")


def p2_parse_input(data: str) -> list:
    grid, moves = data.split("\n\n")

    new_grid = []
    for x, row in enumerate(grid.split("\n")):
        new_row = []
        for y, cell in enumerate(row):
            if cell == "@":
                start = (x, y)
                new_row.append(cell)
                new_row.append(".")
            elif cell in ["#", "."]:
                new_row.append(cell)
                new_row.append(cell)
            elif cell == "O":
                new_row.append("[")
                new_row.append("]")
        new_grid.append(new_row)

    grid_dict = {}
    for x, row in enumerate(new_grid):
        for y, cell in enumerate(row):
            if cell == "@":
                start = (x, y)
            grid_dict[(x, y)] = cell
    moves = moves.replace("\n", "")
    return grid_dict, start, moves


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read()

    print(f"Part1: {part1(data)}")

    grid, start, moves = p2_parse_input(data)

    grid_width, grid_height = max(grid.keys())[0] + 1, max(grid.keys())[1] + 1
    print_grid(grid, grid_width, grid_height)
    x, y = start
    for move in moves:
        print(f"Move: {move}")
        dx, dy = directions[move]
        next_pos = (x + dx, y + dy)

        if grid[next_pos] == "#":
            continue

        elif grid[next_pos] == ".":
            grid[(x, y)] = "."
            grid[next_pos] = "@"
            x, y = next_pos

        elif grid[next_pos] in ["[", "]"]:
            # moving things sideways is much simpler
            # the boxes cannot 'stack' so it just moves them along like a slug
            if move in ["<", ">"]:
                next_box_pos = next_pos
                while grid[next_box_pos] != ".":
                    if grid[next_box_pos] == "#":
                        next_box_pos = (-1, -1)
                        break
                    next_box_pos = (next_box_pos[0] + dx, next_box_pos[1] + dy)

                if next_box_pos[0] != -1 and next_box_pos[1] != -1:
                    new_boxes = tuple(
                        x - y for x, y in zip(next_box_pos, next_pos) if x - y != 0
                    )
                    for i in range(abs(new_boxes[0]) + 1):
                        scaler = 1 if i == 0 else i
                        if move == "<":
                            char = "[" if i % 2 == 0 else "]"
                        elif move == ">":
                            char = "]" if i % 2 == 0 else "["
                        new_box_pos = (
                            next_pos[0] + (dx * scaler),
                            next_pos[1] + (dy * scaler),
                        )
                        grid[new_box_pos] = char

                    grid[next_pos] = "@"
                    grid[(x, y)] = "."
                    x, y = next_pos

            elif move in ["^", "v"]:
                # had to rethink here, the contiguous boxes were confusing me
                # this solution figures out all co-ordinates to move
                # and then moves them all in one fell swoop, using the given direciton
                # of the robot

                blocked = False
                moving_boxes = [(x, y)]
                for i in moving_boxes:
                    new_box_pos = (i[0] + dx, i[1] + dy)

                    if grid[new_box_pos] == "#":
                        blocked = True

                    if new_box_pos in moving_boxes:
                        continue

                    elif grid[new_box_pos] == "[":
                        right_dx, right_dy = directions[">"]
                        box_half = (
                            new_box_pos[0] + right_dx,
                            new_box_pos[1] + right_dy,
                        )
                        moving_boxes.append(new_box_pos)
                        moving_boxes.append(box_half)

                    elif grid[new_box_pos] == "]":
                        left_dx, left_dy = directions["<"]
                        box_half = (new_box_pos[0] + left_dx, new_box_pos[1] + left_dy)
                        moving_boxes.append(new_box_pos)
                        moving_boxes.append(box_half)

                if not blocked:
                    chars = []
                    for i in moving_boxes[1:]:
                        chars.append(grid[i])
                        grid[i] = "."

                    for char, pos in zip(chars, moving_boxes[1:]):
                        new_pos = (pos[0] + dx, pos[1] + dy)
                        grid[new_pos] = char

                    grid[next_pos] = "@"
                    grid[(x, y)] = "."
                    x, y = next_pos
        # print_grid(grid, grid_width, grid_height)
    print(sum_box_coords(grid, "["))


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
