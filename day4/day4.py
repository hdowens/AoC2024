from pathlib import Path


# directions can be
# horizontal, vertical, diagonal, written backwards,
# or even overlapping other words.
def part1(data: list) -> int:
    grid = [list(line) for line in data]
    print_grid = [["."] * len(line) for line in grid]
    str_cnt = 0
    target = "XMAS"

    def bound_check(x, y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def check_sequence(start_line, start_char, direction):
        dx, dy = direction
        for i in range(len(target)):
            nx, ny = start_line + i * dx, start_char + i * dy
            if not bound_check(nx, ny) or grid[nx][ny] != target[i]:
                return False
        return True

    def mark_grid(start_line, start_char, direction):
        dx, dy = direction
        for i, char in enumerate(target):
            nx, ny = start_line + i * dx, start_char + i * dy
            print_grid[nx][ny] = char

    """
    CHECK THE SEQUENCE IN THE GIVEN DIRECTION
           S     S     S            
             A   A   A
               M M M
           S A M X M A S   
               M M M
             A   A   A 
           S     S     S
    """
    directions = {
        "horizontal": (0, 1),
        "reverse horizontal": (0, -1),
        "vertical": (1, 0),
        "reverse vertical": (-1, 0),
        "SE diagonal": (1, 1),
        "SW diagonal": (1, -1),
        "NE diagonal": (-1, 1),
        "NW diagonal": (-1, -1),
    }

    for line_no, line in enumerate(grid):
        for char_no in range(len(line)):
            for name, direction in directions.items():
                if check_sequence(line_no, char_no, direction):
                    mark_grid(line_no, char_no, direction)
                    str_cnt += 1

    # print("\n".join("".join(row) for row in print_grid))
    return str_cnt


def part2(data: list) -> int:
    """
    There are 4 configurations of the X-MAS
    M.S    M.M    S.M    S.S
    .A. -> .A. -> .A. -> .A.
    M.S    S.M    S.M    M.M

    My observation here is that A is always in the middle.
    So my algo will look like:

    For any A found in the grid,
        if -1, -1 == M, if +1,+1 is S and vice versa
        and -1, +1 == S, if +1,-1 is M and vice versa
        then increment the count.

    """
    grid = [list(line) for line in data]

    valid_set = {("M", "S"), ("S", "M")}
    a_count = 0
    # yes X and Y could be used here but I am using line_no and char_no
    for line_no, line in enumerate(grid):
        for char_no, char in enumerate(line):
            if (
                char == "A"
                and 0 < char_no < len(line) - 1
                and 0 < line_no < len(grid) - 1
            ):
                if all(
                    [
                        (grid[line_no - 1][char_no - 1], grid[line_no + 1][char_no + 1])
                        in valid_set,
                        (grid[line_no + 1][char_no - 1], grid[line_no - 1][char_no + 1])
                        in valid_set,
                    ]
                ):
                    a_count += 1

    return a_count


def main() -> None:
    p = Path("test_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().splitlines()

    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
