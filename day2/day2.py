from pathlib import Path


def ascending_or_descending(sq) -> bool:
    if all(
        (sq[i] < sq[i + 1]) and (abs(sq[i] - sq[i + 1]) <= 3)
        for i in range(len(sq) - 1)
    ):
        return True
    elif all(
        (sq[i] > sq[i + 1]) and (abs(sq[i] - sq[i + 1]) <= 3)
        for i in range(len(sq) - 1)
    ):
        return True
    return False


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().splitlines()

    p1_count = 0
    p2_count = 0
    for sequence in data:
        sq = list(map(int, sequence.split()))
        if ascending_or_descending(sq):
            p1_count += 1
        # brute force it
        if any(ascending_or_descending(sq[:i] + sq[i + 1 :]) for i in range(len(sq))):
            p2_count += 1

    print(f"Part 1:\t {p1_count}")
    print(f"Part 2:\t {p2_count}")
    return None


if __name__ == "__main__":
    main()
