from pathlib import Path
from argparse import ArgumentParser
from collections import defaultdict, deque


def print_grid(grid, width, height):
    for x in range(width):
        row = ""
        for y in range(height):
            row += grid[(x, y)]
        print(row)
    print()


def walk(grid, start):
    path = []
    queue = deque([start])
    visited = set()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        pos = queue.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        path.append(pos)
        x, y = pos
        if grid[pos] == "E":
            break
        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if grid.get(next_pos) in ["E", "."] and next_pos not in visited:
                queue.append(next_pos)

    return path


def cheats_under_seconds(path, cheat_seconds, interested_seconds):
    timings = defaultdict(int)
    path_set = set(path)

    for idx, pos in enumerate(path):
        x, y = pos
        for i in range(idx + 1, len(path)):
            x2, y2 = path[i]
            d = abs(x - x2) + abs(y - y2)
            if d <= cheat_seconds and (x2, y2) in path_set:
                sc = (i - idx) - d
                timings[sc] += 1

    return sum(item for key, item in timings.items() if key >= interested_seconds)


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().splitlines()

    grid = {}
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == "S":
                start = x, y
            grid[(x, y)] = data[x][y]

    # we minus one as it counts 'S' and 'E' but in one second it moves from
    # s to first '.' so we need to minus one to get the length of time it takes
    # total_time = sum([1 for value in grid.values() if value != '#']) - 1
    # print(f'Total time without cheats: {total_time}')
    path = walk(grid, start)
    # print(f'Total time without cheats: {len(path) -1 }')
    print(f"Part 1: {cheats_under_seconds(path, 2, 100)}")
    print(f"Part 2: {cheats_under_seconds(path, 20, 100)}")


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


"""  
Wanted to leave this in, in posterity.
"""
# def part1(grid, path):
#    #we have a function to 'walk' the path, it returns the path
#    #now based on the condition of a shortcut , move the path to the shortcut
#    #and remove the intermediary steps
#    #         .
#    #         .
#    #       ##S#.
#    #         #
#    #         #
#    #The shape of  S#., where S is any position currently at in the path, with wall
#    #then a path component, is my first guess of a shortcut. I dont observe any other
#    #formations in the test case so will use that and see what happens. So, when that is seen
#    #figure out it's index in the path, remove intermediary and compute the length
#    #of the new path, then figure out the difference and we have our saved seconds
#    visited = set()
#    timings = defaultdict(int)
#    for pos in path:
#        x, y = pos
#        visited.add(pos)
#
#        # Check the four directions twice
#        if grid.get((x, y+1)) == '#' and grid.get((x, y+2)) in ['E', '.'] and (x, y+2) not in visited:
#            sc = path.index((x, y+2)) - path.index((x, y)) - 2
#            if sc > 0:
#                timings[sc] += 1
#        if grid.get((x, y-1)) == '#' and grid.get((x, y-2)) in ['E', '.'] and (x, y-2) not in visited:
#            sc = path.index((x, y-2)) - path.index((x, y)) - 2
#            if sc > 0:
#                timings[sc] += 1
#
#        if grid.get((x+1, y)) == '#' and grid.get((x+2, y)) in ['E', '.'] and (x+2, y) not in visited:
#            sc = path.index((x+2, y)) - path.index((x, y)) - 2
#            if sc > 0:
#                timings[sc] += 1
#
#        if grid.get((x-1, y)) == '#' and grid.get((x-2, y)) in ['E', '.'] and (x-2, y) not in visited:
#            sc = path.index((x-2, y)) - path.index((x, y)) - 2
#            if sc > 0:
#                timings[sc] += 1
#
#    #for key, item in timings.items():
#    #    print(f'Shortcut of {key} seconds found {item} times')
#
#    return sum([item for key, item in timings.items() if key >= 100])
