from pathlib import Path


def part1(data):
    count = 0

    def traverse(x, y, height, data):
        if x < 0 or y < 0 or x >= len(data) or y >= len(data[0]):
            return  # out of bounds

        if data[x][y] != str(height):
            return

        if data[x][y] == "9":
            max_height_positions.add((x, y))
            return

        traverse(x + 1, y, height + 1, data)  # down
        traverse(x - 1, y, height + 1, data)  # up
        traverse(x, y + 1, height + 1, data)  # right
        traverse(x, y - 1, height + 1, data)  # left

    for x, line in enumerate(data):
        for y, row in enumerate(line):
            if data[x][y] == "0":
                max_height_positions = set()
                traverse(x, y, 0, data)
                count += len(max_height_positions)

    return count


def part2(data):
    count = 0

    def traverse(x, y, height, data):
        nonlocal count

        if x < 0 or y < 0 or x >= len(data) or y >= len(data[0]):
            return  # out of bounds

        if data[x][y] != str(height):
            return

        if data[x][y] == "9":
            count += 1
            return

        traverse(x + 1, y, height + 1, data)  # down
        traverse(x - 1, y, height + 1, data)  # up
        traverse(x, y + 1, height + 1, data)  # right
        traverse(x, y - 1, height + 1, data)  # left

    for x, line in enumerate(data):
        for y, row in enumerate(line):
            if data[x][y] == "0":
                traverse(x, y, 0, data)
    return count


def main():
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as f:
        data = f.read().splitlines()

    trail_head_count = part1(data)
    print(f"Trail head score: {trail_head_count}")
    distinct_trail = part2(data)
    print(f"Distinct trails : {distinct_trail}")


if __name__ == "__main__":
    main()
