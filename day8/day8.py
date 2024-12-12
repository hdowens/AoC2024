from pathlib import Path
from itertools import combinations


def find_attena(data: list, char: str) -> str:
    ret = []
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == char:
                ret.append((x, y))
    return ret


def bounds_check(x: int, y: int, data: list) -> bool:
    return x >= 0 and y >= 0 and x < len(data) and y < len(data[0])


def part1(data, frequencies):
    antinodes_placed = set()
    for freq in frequencies:
        alst = find_attena(data, freq)

        for previous, current in combinations(alst, 2):
            dx, dy = current[0] - previous[0], current[1] - previous[1]
            an_1 = (previous[0] - dx, previous[1] - dy)
            an_2 = (current[0] + dx, current[1] + dy)

            if bounds_check(an_1[0], an_1[1], data) and data[an_1[0]][an_1[1]] != freq:
                antinodes_placed.add(an_1)

            if bounds_check(an_2[0], an_2[1], data) and data[an_2[0]][an_2[1]] != freq:
                antinodes_placed.add(an_2)

    return len(antinodes_placed)


def part2(data, frequencies):
    antinodes_placed = set()
    for freq in frequencies:
        alst = find_attena(data, freq)

        for previous, current in combinations(alst, 2):
            dx, dy = current[0] - previous[0], current[1] - previous[1]
            an_1 = (previous[0] - dx, previous[1] - dy)
            an_2 = (current[0] + dx, current[1] + dy)

            while bounds_check(an_1[0], an_1[1], data) or bounds_check(
                an_2[0], an_2[1], data
            ):
                if (
                    bounds_check(an_1[0], an_1[1], data)
                    and data[an_1[0]][an_1[1]] != freq
                ):
                    antinodes_placed.add(an_1)

                if (
                    bounds_check(an_2[0], an_2[1], data)
                    and data[an_2[0]][an_2[1]] != freq
                ):
                    antinodes_placed.add(an_2)

                an_1, an_2 = (an_1[0] - dx, an_1[1] - dy), (an_2[0] + dx, an_2[1] + dy)

        antinodes_placed.update(alst)

    return len(antinodes_placed)


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().splitlines()

    frequencies = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    print(f"Part 1: {part1(data, frequencies)}")
    print(f"Part 2: {part2(data, frequencies)}")


if __name__ == "__main__":
    main()
