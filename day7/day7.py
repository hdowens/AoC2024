import re
from enum import Enum
from pathlib import Path


class Operator(Enum):
    ADD = "+"
    MUL = "*"
    CONCAT = "||"


def hit_target(candidates, target, current_result=0, index=0, operators=[]):
    # check if we hit that target at the end
    if index == len(candidates):
        return current_result == target

    results = []
    if Operator.ADD in operators:
        results.append(
            hit_target(
                candidates,
                target,
                current_result + candidates[index],
                index + 1,
                operators,
            )
        )
    if Operator.MUL in operators:
        results.append(
            hit_target(
                candidates,
                target,
                current_result * candidates[index],
                index + 1,
                operators,
            )
        )
    if Operator.CONCAT in operators:
        results.append(
            hit_target(
                candidates,
                target,
                int(str(current_result) + str(candidates[index])),
                index + 1,
                operators,
            )
        )

    return any(results)


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().splitlines()

    total_hit = 0
    total_cat_hit = 0

    p1_ops = [Operator.ADD, Operator.MUL]
    p2_ops = [Operator.ADD, Operator.MUL, Operator.CONCAT]

    for line in data:
        target, candidates = line.split(":")
        candidates = list(map(int, re.findall(r"(\d+)", candidates)))
        # print(f"Target: {target}, from: {candidates}")
        if hit_target(candidates, int(target), candidates[0], 1, p1_ops):
            # print(f"\t[+]Target {target} can be hit.")
            total_hit += int(target)
        else:
            # print(f"\t[-]Target {target} cannot be hit.")
            if hit_target(candidates, int(target), candidates[0], 1, p2_ops):
                # print(f"\t[+]Target {target} can be hit with concatenation.")
                total_cat_hit += int(target)
    print(f"Total p1: {total_hit}")
    print(f"Total p2: {total_hit + total_cat_hit}")


if __name__ == "__main__":
    main()
