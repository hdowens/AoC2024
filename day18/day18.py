import heapq
import re
from argparse import ArgumentParser
from pathlib import Path

directions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "RIGHT": (0, 1),
    "LEFT": (0, -1),
}


def parse_input(data: list, grid_size, sim_size):
    coords = [tuple(map(int, re.findall(r"\d+", c))) for c in data][:sim_size]
    grid_map = {}
    for c in range(grid_size):
        for r in range(grid_size):
            if (r, c) in coords:
                grid_map[(r, c)] = "#"
            else:
                grid_map[(r, c)] = "."
    return grid_map, coords


def manhattan_distance(point1: tuple, point2: tuple) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def print_grid(grid):
    max_x = max(x for x, y in grid.keys())
    max_y = max(y for x, y in grid.keys())

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid.get((x, y)), end="")
        print()


def a_star(grid: dict, start_pos: tuple, visited: set, grid_size: int) -> int:
    queue = []
    origin = {}
    origin[start_pos] = None
    heapq.heappush(queue, (0, 0, start_pos))  # heurisitc, steps, position

    while queue:
        _, steps, (cur_x, cur_y) = heapq.heappop(queue)

        if (cur_x, cur_y) == (grid_size - 1, grid_size - 1):
            return steps

        for dx, dy in directions.values():
            next_pos = (cur_x + dx, cur_y + dy)
            if next_pos not in origin and grid.get(next_pos) == ".":
                origin[next_pos] = (cur_x, cur_y)
                heur = manhattan_distance(next_pos, (grid_size - 1, grid_size - 1))
                new_cost = steps + heur + 1
                heapq.heappush(queue, (new_cost, steps + 1, next_pos))
    return -1


def part1(data, grid_size, sim_size):
    grid, _ = parse_input(data, grid_size, sim_size)
    return a_star(grid, (0, 0), set(), grid_size)


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().splitlines()

    grid_size = 71
    print(f"Part 1: {part1(data, grid_size, 1024)}")
    for sim_sz in range(0, grid_size * grid_size):
        grid, coords = parse_input(data, grid_size, sim_sz)
        if a_star(grid, (0, 0), set(), grid_size) == -1:
            print(f"Found sim size: {sim_sz}, co-ord: {coords[sim_sz - 1]}")
            break


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
