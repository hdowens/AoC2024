from pathlib import Path
import re
from argparse import ArgumentParser


GRID_WIDTH = 101
GRID_HEIGHT = 103


def print_grid(grid, width, height):
    for y in range(height):
        row = ""
        for x in range(width):
            val = grid[(x, y)]
            if val == 0:
                row += "."
            else:
                row += str(val)
        print(row)


def quad_sum(grid) -> int:
    mid_row = GRID_HEIGHT // 2
    mid_col = GRID_WIDTH // 2

    quadrants = {"top_left": 0, "top_right": 0, "bottom_left": 0, "bottom_right": 0}

    # print_grid(grid, GRID_WIDTH, GRID_HEIGHT)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if x == mid_col or y == mid_row:
                # print(' ', end='')
                continue

            val = int(grid[(x, y)])
            if x < mid_col and y < mid_row:
                # print('A', end='')
                if val > 0:
                    quadrants["top_left"] += val
            elif x < mid_col and y > mid_row:
                # print('B', end='')
                if val > 0:
                    quadrants["top_right"] += val
            elif x > mid_col and y < mid_row:
                # print('C', end='')
                if val > 0:
                    quadrants["bottom_left"] += val
            elif x > mid_col and y > mid_row:
                # print('D', end='')
                if val > 0:
                    quadrants["bottom_right"] += val

    return quadrants


# this was my first guess, cant really believe it worked lol
def part2_check(grid) -> bool:
    return all(
        grid[(x, y)] in (0, 1) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)
    )


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().splitlines()

    positions = [
        tuple(map(int, pos))
        for pos in [re.findall(r"p=(\d+),(\d+)", item)[0] for item in data]
    ]
    vectors = [
        tuple(map(int, pos))
        for pos in [re.findall(r"v=(-?\d+),(-?\d+)", pos)[0] for pos in data]
    ]

    assert len(positions) == len(vectors)

    grid = {}
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            grid[(x, y)] = 0

    for pos in positions:
        grid[pos] += 1

    # print_grid(grid, GRID_WIDTH, GRID_HEIGHT)
    # print(f'Num bots: {sum(i for i in grid.values() if i >= 1)}')

    for i in range(0, 50000):
        for pos, movement in zip(positions, vectors):
            grid[pos] -= 1
            pos = (
                (pos[0] + movement[0]) % GRID_WIDTH,
                (pos[1] + movement[1]) % GRID_HEIGHT,
            )
            grid[pos] += 1

        # the positions also need to be reset to the new set of positions
        # because they are zipped with the vectors, they need to remain in
        # exactly the same order
        if part2_check(grid):
            print(f"Part 2: {i+1}")

        tmp = []
        for pos, movement in zip(positions, vectors):
            pos = (
                (pos[0] + movement[0]) % GRID_WIDTH,
                (pos[1] + movement[1]) % GRID_HEIGHT,
            )
            tmp.append(pos)

        positions = tmp

    # print(f'Num bots: {sum(i for i in grid.values() if i >= 1)}')
    quads = quad_sum(grid)
    prod = 1
    for val in quads.values():
        prod *= val
    print(f"Num bots in quads: {sum(i for i in grid.values() if i >= 1)}")
    print(f"Safety rating: {prod}")


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
