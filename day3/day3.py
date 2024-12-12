import re
from functools import reduce
from pathlib import Path

P1_TEST_STRING = (
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
)
P2_TEST_STRING = (
    """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
)


def find_matching_strings(text):
    pattern = r"mul\(\b\d{1,3}\b,\b\d{1,3}\b\)"
    return re.findall(pattern, text), re.finditer(pattern, text)


def find_dos(text):
    pattern = r"do\(\)"
    return re.finditer(pattern, text)


def find_donts(text):
    pattern = r"don\'t\(\)"
    return re.finditer(pattern, text)


def sum_matching_pairs(pairs):
    return reduce(
        lambda acc, pair: acc + int(pair.split(",")[0]) * int(pair.split(",")[1]),
        pairs,
        0,
    )


def find_safe_ranges(dos, donts, text_length):
    safe_ranges = []
    current_start = 0
    in_safe_range = True

    events = sorted(dos + donts, key=lambda x: x[0])

    for event in events:
        if in_safe_range:
            if event in donts:
                safe_ranges.append((current_start, event[0]))
                in_safe_range = False
        else:
            if event in dos:
                current_start = event[1]
                in_safe_range = True

    if in_safe_range:
        safe_ranges.append((current_start, text_length))

    return safe_ranges


def values_in_safe_ranges(p_list, safe_ranges):
    safe_values = []
    for start, end in safe_ranges:
        for idx, pos in enumerate(p_list):
            if start <= pos[0] < end:
                safe_values.append(idx)
    return safe_values


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read()

    numbers, positions = find_matching_strings(data)
    pairs = re.findall(r"(\d+,\d+)", "".join(i for i in numbers))
    print(f"Part 1: {sum_matching_pairs(pairs)}")

    dos = [(m.start(0), m.end(0)) for m in find_dos(data)]
    donts = [(m.start(0), m.end(0)) for m in find_donts(data)]
    p_list = [(m.start(0), m.end(0)) for m in positions]

    safe_ranges = find_safe_ranges(dos, donts, len(data))
    safe_vals = [pairs[x] for x in values_in_safe_ranges(p_list, safe_ranges)]
    print(f"Part 2: {sum_matching_pairs(safe_vals)}")

    """
    This is to learn from others on their regex

    Found this online from day3: 
    pattern = re.compile(r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)')

    Use the `|` bars to represent OR statements in the REGEX. Goddamit.
    """


if __name__ == "__main__":
    main()
