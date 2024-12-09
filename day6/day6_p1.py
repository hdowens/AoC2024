from pathlib import Path

def find_char(data: list, wanted: str) -> tuple:
    for x, row in enumerate(data):
        for y, char in enumerate(row):
            if char == wanted:
                return x, y
    return -1, -1

def move_in_direction(data, print_grid, front_of_path, dx, dy):
    x, y = front_of_path
    while 0 <= x < len(data) and 0 <= y < len(data[0]):
        if data[x][y] == '#':
            return (x - dx, y - dy), False
        elif (dx == -1 and x == 0) or (dx == 1 and x == len(data) - 1) or (dy == -1 and y == 0) or (dy == 1 and y == len(data[0]) - 1):
            print_grid[x][y] = 'X'
            return (x, y), True
        print_grid[x][y] = 'X'
        x += dx
        y += dy
    return (x, y), False

def part1(data: list) -> int:
    print_grid = [list(line) for line in data]
    directions = {
        0 : (-1, 0),
        1 : (0, 1),
        2 : (1, 0),
        3 : (0, -1),
    }

    order_counter = 0
    front_of_path = find_char(data, '^')
    dx, dy = directions[order_counter]
    bounds_flag = False

    while not bounds_flag:
        front_of_path, bounds_flag = move_in_direction(data, print_grid, front_of_path, dx, dy)
        if not bounds_flag:
            order_counter = (order_counter + 1) % 4
            dx, dy = directions[order_counter]

    ans = "".join("".join(row) for row in print_grid).count('X')
    guard_start = find_char(data, '^')
    #print("\n".join("".join(row) for row in print_grid))
    print_grid[guard_start[0]][guard_start[1]] = "^"
    return ans


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().splitlines()

    print(f"Part 1: {part1(data)}")


if __name__ == "__main__":
    main()