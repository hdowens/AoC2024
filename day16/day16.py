from pathlib import Path
from argparse import ArgumentParser
import heapq

directions = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}

# need to be able to iterate over
directions_list = ["^", ">", "v", "<"]


def parse_grid(grid: str) -> dict:
    grid_dict = {}
    for x, row in enumerate(grid.split("\n")):
        for y, cell in enumerate(row):
            if cell == "S":
                start = x, y
            grid_dict[(x, y)] = cell
    return grid_dict, start


def print_grid(grid, unique_tiles):
    # Find grid dimensions
    max_x = max(x for x, y in grid.keys())
    max_y = max(y for x, y in grid.keys())

    for x in range(max_x + 1):
        for y in range(max_y + 1):
            pos = (x, y)
            if pos in unique_tiles:
                print("O", end="")  # Tile is part of an optimal path
            elif grid.get(pos) == "#":
                print("#", end="")  # Wall
            else:
                print(".", end="")  # Empty space
        print()  # New line


def dijsktra(grid: dict, start_pos: tuple) -> set:
    pqueue = [(0, start_pos, ">")]
    seen = set({start_pos, ">"})

    while pqueue:
        cost, pos, dir = heapq.heappop(pqueue)
        seen.add((pos, dir))
        if grid.get(pos) == "E":
            return cost
        # FORWARD, LEFT OR RIGHT
        for move in ("F", "L", "R"):
            new_pos = pos
            new_dir = dir

            if move == "F":
                direction = directions[dir]
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                new_cost = cost + 1
            else:
                new_dir = (
                    directions_list[(directions_list.index(dir) + 1) % 4]
                    if move == "R"
                    else directions_list[(directions_list.index(dir) - 1) % 4]
                )
                new_cost = cost + 1000

            if grid.get(new_pos) == "#":
                continue

            if (new_pos, new_dir) not in seen:
                heapq.heappush(pqueue, (new_cost, new_pos, new_dir))

    assert False, "No path found"


def dijkstra_all_paths(grid: dict, start_pos: tuple) -> tuple[list, int, set]:
    pqueue = [(0, start_pos, ">", [(start_pos, ">")])]
    seen = {}  # (pos, dir) -> cost
    optimal_paths = []
    min_end_cost = float("inf")

    while pqueue:
        cost, pos, dir, path = heapq.heappop(pqueue)

        # If we've found a path to the end
        if grid.get(pos) == "E":
            if cost < min_end_cost:
                # Found a better path, clear previous paths
                optimal_paths = [path]
                min_end_cost = cost
            elif cost == min_end_cost:
                # Found another optimal path
                optimal_paths.append(path)
            continue

        if (pos, dir) in seen and seen[(pos, dir)] < cost:
            continue

        seen[(pos, dir)] = cost

        for move in ("F", "L", "R"):
            new_pos = pos
            new_dir = dir

            if move == "F":
                direction = directions[dir]
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                new_cost = cost + 1
            else:
                new_dir = (
                    directions_list[(directions_list.index(dir) + 1) % 4]
                    if move == "R"
                    else directions_list[(directions_list.index(dir) - 1) % 4]
                )
                new_cost = cost + 1000

            # Skip if hitting wall
            if grid.get(new_pos) == "#":
                continue

            # Only explore if:
            # 1. We haven't seen this state before, or
            # 2. We've found a better cost to reach this state
            if (new_pos, new_dir) not in seen or new_cost < seen[(new_pos, new_dir)]:
                new_path = path + [(new_pos, new_dir)]
                heapq.heappush(pqueue, (new_cost, new_pos, new_dir, new_path))

    if not optimal_paths:
        raise ValueError("No path found")

    # Extract unique tiles from all optimal paths
    unique_tiles = set()
    for path in optimal_paths:
        # Add only the positions (not the directions) to our set of unique tiles
        unique_tiles.update(pos for pos, _ in path)

    return unique_tiles


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read()

    grid, start = parse_grid(data)

    optimal_cost = dijsktra(grid, start)
    print(f"Optimal path cost: {optimal_cost}")

    unique_tiles = dijkstra_all_paths(grid, start)
    print(f"Optimal paths cover {len(unique_tiles)} unique tiles")


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
