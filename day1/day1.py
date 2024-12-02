from collections import Counter


def main() -> None:
    with open("puz_input.txt", "r") as input:
        data = input.read().splitlines()

    first_list, second_list = zip(*(map(int, line.split()) for line in data))
    p1_ans = sum(abs(f - s) for f, s in zip(sorted(first_list), sorted(second_list)))
    print(f"Part 1: {p1_ans}")

    # have used a sneaky import here
    counted = Counter(second_list)
    p2_ans = sum(counted[item] * item for item in first_list)
    print(f"Part 2: {p2_ans}")

    # someone else did:
    # print(sum(x for x in l2 if x in l1)) which is pretty cool

    return None


if __name__ == "__main__":
    main()
