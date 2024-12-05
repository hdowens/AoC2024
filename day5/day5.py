from pathlib import Path


def part1(rules, instructions) -> int:
    total = 0
    for it in instructions:
        err_flag = True
        for i in range(0, len(it)):
            for j in range(i + 1, len(it)):
                if (it[j], it[i]) in rules and err_flag:
                    err_flag = False

        if err_flag:
            total += it[(len(it) - 1) // 2]

    return total


def part2(rules, instructions) -> int:
    new_insrts = []
    for it in instructions:
        err_flag = True
        for i in range(0, len(it)):
            for j in range(i + 1, len(it)):
                if (it[j], it[i]) in rules:
                    err_flag = False
                    it[j], it[i] = it[i], it[j]

        if not err_flag:
            new_insrts.append(it)

    return sum(it[(len(it) - 1) // 2] for it in new_insrts)


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().split("\n\n")

    # lets transform the rules into a list of tuples
    rules = [tuple(map(int, s.split("|"))) for s in data[0].split("\n")]

    # lets transform the instructions into a list of list of integers
    instructions = [list(map(int, sample.split(","))) for sample in data[1].split("\n")]

    print(f"Part 1: {part1(rules, instructions)}")
    print(f"Part 2: {part2(rules, instructions)}")


if __name__ == "__main__":
    main()
