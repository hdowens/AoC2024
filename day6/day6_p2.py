from pathlib import Path

directions = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}


def find_char(data: list, wanted: str) -> tuple:
    for x, row in enumerate(data):
        for y, char in enumerate(row):
            if char == wanted:
                return x, y
    return -1, -1


def look_ahead(lab_map, pos):
    try:
        if pos[0] < 0 or pos[1] < 0:
            return None
        return lab_map[pos[0]][pos[1]]
    except IndexError:
        return None


def cycle_check(lab_map, loc_i, loc_j, bound_i, bound_j, dir_cnt):
    loc_rotation_path = set()
    dire = directions[dir_cnt]
    while 0 <= loc_i < bound_i and 0 <= loc_j < bound_j:
        while look_ahead(lab_map, [loc_i + dire[0], loc_j + dire[1]]) == "#":
            dire = directions[dir_cnt]
            seen_location_set = (loc_i, loc_j, dire[0], dire[1])
            if seen_location_set in loc_rotation_path:
                return True
            loc_rotation_path.add(seen_location_set)
            dir_cnt = (dir_cnt + 1) % 4
        loc_i += dire[0]
        loc_j += dire[1]
    return False


def move_guard(guard_map, guard_x, guard_y, dir_cnt):
    next_pos = guard_x + directions[dir_cnt][0], guard_y + directions[dir_cnt][1]
    if look_ahead(guard_map, [next_pos[0], next_pos[1]]) is None:
        return guard_x, guard_y, dir_cnt, True
    if guard_map[next_pos[0]][next_pos[1]] == "#":
        dir_cnt = (dir_cnt + 1) % 4
    return (
        guard_x + directions[dir_cnt][0],
        guard_y + directions[dir_cnt][1],
        dir_cnt,
        False,
    )


def part2(data: list) -> int:
    guard_map = [list(line) for line in data]
    start = find_char(data, "^")
    guard_x, guard_y = start

    dir_cnt = 0
    cycle_count = 0
    while 0 <= guard_x < len(guard_map) and 0 <= guard_y < len(guard_map[0]):
        guard_x, guard_y, dir_cnt, out_of_bounds = move_guard(
            guard_map, guard_x, guard_y, dir_cnt
        )
        if out_of_bounds:
            break

        if guard_map[guard_x][guard_y] == ".":
            guard_map[guard_x][guard_y] = "#"
            cycle_count += cycle_check(
                guard_map, guard_x, guard_y, len(guard_map), len(guard_map[0]), dir_cnt
            )
            guard_map[guard_x][guard_y] = ""

    return cycle_count


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().splitlines()

    print(f"Part 2: {part2(data)}")


if __name__ == "__main__":
    main()
