from pathlib import Path
from argparse import ArgumentParser
from collections import deque


def sorted_type_gates(wire_states: dict, type: str) -> dict:
    type_gates = {key: val for key, val in wire_states.items() if key.startswith(type)}
    return dict(sorted(type_gates.items(), key=lambda item: int(item[0][1:])))


def extract_dec(wire_states: dict, prefix: str):
    sorted_gates = sorted_type_gates(wire_states, prefix)
    num_str = "".join(
        reversed([str(val) for key, val in sorted_gates.items() if key[0] == prefix])
    )
    return int(num_str, 2)


def simulate_logic(wire_states, conditions):
    while conditions:
        condition = conditions.popleft()
        parts = condition.split(" ")
        wire1, op, wire2 = parts[0], parts[1], parts[2]
        val1 = wire_states.get(wire1)
        val2 = wire_states.get(wire2)

        if val1 is None or val2 is None:
            conditions.append(condition)
            continue

        if op == "AND":
            wire_states[parts[-1]] = val1 & val2
        elif op == "OR":
            wire_states[parts[-1]] = val1 | val2
        elif op == "XOR":
            wire_states[parts[-1]] = val1 ^ val2
    return wire_states


def determine_expected_outputs_sum(wire_states):
    x_number = extract_dec(wire_states, "x")
    y_number = extract_dec(wire_states, "y")
    sum_number = x_number + y_number
    binary_sum = bin(sum_number)[2:][::-1]

    expected_outputs = {}
    for i, bit in enumerate(binary_sum):
        expected_outputs[f"z{i:02}"] = int(bit)
    return expected_outputs


def determine_expected_outputs_and(wire_states):
    x_number = extract_dec(wire_states, "x")
    y_number = extract_dec(wire_states, "y")
    sum_number = x_number & y_number
    binary_sum = bin(sum_number)[2:][::-1]

    expected_outputs = {}
    for i, bit in enumerate(binary_sum):
        expected_outputs[f"z{i:02}"] = int(bit)
    return expected_outputs


def part1(wire_states: dict, logic: list) -> int:
    conditions = deque(logic.splitlines())

    wire_states = simulate_logic(wire_states, conditions)

    z_gates = {key: val for key, val in wire_states.items() if key.startswith("z")}
    sorted_z_gates = dict(sorted(z_gates.items(), key=lambda item: int(item[0][1:])))

    b_ans = "".join(
        reversed([str(val) for key, val in sorted_z_gates.items() if key[0] == "z"])
    )
    # print(f'Ans: [b]: {b_ans} \t[d]: {int(b_ans, 2)}')
    return int(b_ans, 2)


def pp(formula, wire, depth=0):
    if wire[0] in "xy":
        return "  " * depth + wire
    op, x, y = formula[wire]
    return (
        "  " * depth
        + op
        + f" ({wire})\n"
        + pp(formula, x, depth + 1)
        + "\n"
        + pp(formula, y, depth + 1)
    )


def veryify_int_xor(wire, num, formulas):
    op, x, y = formulas[wire]
    if op != "XOR":
        return False
    return x == f"x{num:02}" and y == f'f"y{num:02}"'


def verify_carry(wire, num, formulas):
    op, x, y = formulas[wire]
    if num == 1:
        if op != "AND":
            return False
        return x == f"x{num:02}" and y == f'f"y{num:02}"'
    if op != "OR":
        return False
    return (
        verify_d_carry(x, num - 1, formulas)
        and verify_r_carry(y, num - 1, formulas)
        or verify_d_carry(y, num - 1, formulas)
        and verify_r_carry(x, num - 1, formulas)
    )


def verify_d_carry(wire, num, formulas):
    op, x, y = formulas[wire]
    if op != "AND":
        return False
    return x == f"x{num:02}" and y == f'f"y{num:02}"'


def verify_r_carry(wire, num, formulas):
    op, x, y = formulas[wire]
    if op != "AND":
        return False
    return (
        veryify_int_xor(x, num)
        and verify_carry(y, num)
        or veryify_int_xor(y, num)
        and verify_carry(x, num)
    )


def verify_z(wire, num, formulas):
    print("vz", wire, num)
    op, x, y = formulas[wire]
    # z has to be equal to X XOR Y
    if op != "XOR":
        return False
    if num == 0:
        return x == "x00" and y == "y00"

    return (
        veryify_int_xor(x, num, formulas)
        and verify_carry(y, num, formulas)
        or veryify_int_xor(y, num, formulas)
        and verify_carry(x, num, formulas)
    )
    # we need to verify intermediate xor gates


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        states, logic = file.read().split("\n\n")

    wire_states = {}
    for state in states.splitlines():
        wire, value = state.split(": ")
        wire_states[wire] = int(value)

    # print(f'Part 1: {part1(wire_states, logic)}')

    # part 2
    formulae = {}
    for line in logic.splitlines():
        x, op, y, z = line.replace(" ->", " ").split()
        formulae[z] = (op, x, y)

    def verify(num):
        return verify_z(f"z{num:02}", num, formulae)

    print(verify(5))

    # expected_output = determine_expected_outputs_sum(wire_states)
    # print('X', ''.join([str(val) for val in x_gates.values()]))
    # print('Y', ''.join([str(val) for val in y_gates.values()]))
    # ans = ''.join([str(val) for val in expected_output.values()])
    # print('-'*len(ans))
    # print('ans', ans)
    # conditions = deque(logic.splitlines())
    # wire_states = simulate_logic(wire_states, conditions)
    # z_gates = {key: val for key, val in wire_states.items() if key.startswith('z')}
    # sorted_z_gates = dict(sorted(z_gates.items(), key=lambda item: int(item[0][1:])))


#
# b_ans = ''.join(reversed([str(val) for key, val in sorted_z_gates.items() if key[0] == 'z']))
# print('sim',  b_ans)
#
# info = []
# for ans, sim in zip(ans, b_ans):
#    if ans != sim:
#        info.append('^')
#    else:
#        info.append(' ')
# print(''.join(info))


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t", "--test", action="store_true", help="Read from test_input.txt"
    )
    group.add_argument(
        "-p", "--puzzle", action="store_true", help="Read from puz_input.txt"
    )

    args = parser.parse_args()

    if args.test:
        file_path = Path("test_input.txt")
    elif args.puzzle:
        file_path = Path("puz_input.txt")

    main(file_path)
