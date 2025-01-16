from pathlib import Path
from argparse import ArgumentParser
from collections import deque

directions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "RIGHT": (0, 1),
    "LEFT": (0, -1),
}


def bfs(grid: dict, start_pos: tuple, visited: set) -> set:
    queue = deque([start_pos])
    region = set([start_pos])
    visited.add(start_pos)

    while queue:
        cur_x, cur_y = queue.popleft()
        for dx, dy in directions.values():
            next_pos = (cur_x + dx, cur_y + dy)
            if next_pos not in visited and grid.get(next_pos) == grid[cur_x, cur_y]:
                queue.append(next_pos)
                visited.add(next_pos)
                region.add(next_pos)
    return region


def get_region_and_area(region: set[(tuple)]) -> int:
    area = len(region)
    perimeter = 0
    for x, y in region:
        for dx, dy in directions.values():
            neighbor = (x + dx, y + dy)
            if neighbor not in region:
                perimeter += 1
    return area * perimeter


def get_region_and_area_discount(region: set[tuple[int, int]]) -> int:
    area = len(region)
    sides = 0

    for x, y in region:
        corners = 0
        neighbors = [
            (x + dx, y + dy)
            for dx, dy in directions.values()
            if (x + dx, y + dy) in region
        ]

        if len(neighbors) == 0:
            corners += 4
        elif len(neighbors) == 1:
            corners += 2
        elif len(neighbors) == 2:
            if all(n[0] == x for n in neighbors) or all(n[1] == y for n in neighbors):
                continue
            else:
                if (neighbors[0][0], neighbors[1][1]) in region:
                    corners += 1
                else:
                    corners += 2
        elif len(neighbors) == 3:
            if all(n[0] == x for n in neighbors) or all(n[1] == y for n in neighbors):
                continue
            if (
                sum(n[0] == x for n in neighbors) == 2
                and sum(n[1] == y for n in neighbors) == 1
            ):
                outlier = [n for n in neighbors if n[1] == y][0]
                to_check = [(outlier[0], n[1]) for n in neighbors if n[1] != y]
                for n in to_check:
                    if n not in region:
                        corners += 1
            if (
                sum(n[0] == x for n in neighbors) == 1
                and sum(n[1] == y for n in neighbors) == 2
            ):
                outlier = [n for n in neighbors if n[0] == x][0]
                to_check = [(n[0], outlier[1]) for n in neighbors if n[0] != x]
                for n in to_check:
                    if n not in region:
                        corners += 1
        elif len(neighbors) == 4:
            diagonals = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
            for dx, dy in diagonals:
                if (x + dx, y + dy) not in region:
                    corners += 1

        sides += corners

    return area * sides


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().splitlines()

    # need to parse in the entire grid to a dictionary
    grid = {}
    for x, row in enumerate(data):
        for y, char in enumerate(row):
            grid[(x, y)] = char

    regions = []
    visited = set()
    for x in range(len(data)):
        for y in range(len(data[0])):
            if (x, y) not in visited:
                region = bfs(grid, (x, y), visited)
                regions.append(region)

    print(f"Part 1: {sum(get_region_and_area(region) for region in regions)}")
    print(f"Part 1: {sum(get_region_and_area_discount(region) for region in regions)}")


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
