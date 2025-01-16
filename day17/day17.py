from pathlib import Path
from argparse import ArgumentParser
import re


def parse_input(file_path: Path):
    with open(file_path, "r") as file:
        registers, instructions = file.read().split("\n\n")

    # we have three registers, A B C
    keys = ["A", "B", "C"]
    values = map(int, re.findall(r"\d+", registers))
    reg_states = dict(zip(keys, values))
    program = list(map(int, re.findall(r"\d+", instructions)))
    return reg_states, program


def do_operation(
    opcode: int, operand: int, registers: dict, out: list, pc: int
) -> dict:
    combo_operand = operand
    if operand == 4:
        combo_operand = registers["A"]
    elif operand == 5:
        combo_operand = registers["B"]
    elif operand == 6:
        combo_operand = registers["C"]

    # now do the instruction
    if opcode == 0:
        # here he have the division operation
        registers["A"] = (registers["A"]) // (2**combo_operand)
        pc += 2

    elif opcode == 1:
        # here we have the bitwise XOR operation
        registers["B"] = registers["B"] ^ operand
        pc += 2

    elif opcode == 2:
        # here we have the 'bst' instruction
        # modulo 8 with the operand and write to register B
        registers["B"] = combo_operand % 8
        pc += 2

    elif opcode == 3:
        # do nothing if register A is 0
        if registers["A"] == 0:
            return registers, pc + 2
        pc = operand

    elif opcode == 4:
        # here we have the 'bxc' instruction
        # bitwise or between A and B
        registers["B"] = registers["B"] ^ registers["C"]
        pc += 2

    elif opcode == 5:
        # here we have the out instruction
        out.append(combo_operand % 8)
        pc += 2

    elif opcode == 6:
        # here he have the division operation
        registers["B"] = (registers["A"]) // (2**combo_operand)
        pc += 2

    elif opcode == 7:
        # here he have the division operation
        registers["C"] = (registers["A"]) // (2**combo_operand)
        pc += 2

    return registers, pc


def simulate(registers: dict, program: list, thresh=None) -> str:
    out = []
    pc = 0
    while pc < len(program):
        if thresh is not None and len(out) == thresh:
            return out

        opcode = program[pc]
        operand = program[pc + 1]
        registers, pc = do_operation(opcode, operand, registers, out, pc)

    return out


# reverse engineeried my input to get the solution
def part2(program, ans):
    if program == []:
        return ans
    for b in range(8):
        a = ans << 3 | b
        b = a % 8
        b = b ^ 1
        c = a >> b
        b = b ^ 5
        b = b ^ c
        if b % 8 == program[-1]:
            sub_soln = part2(program[:-1], a)
            if sub_soln is None:
                continue
            return sub_soln


def main(file_path: Path) -> None:
    registers, program = parse_input(file_path)

    print(f"Part 1: {','.join(str(i) for i in simulate(registers, program))}")
    # a_value = 10**(len(program))

    print(f"Part 2: {part2(program, 0)}")


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
