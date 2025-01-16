from pathlib import Path
from argparse import ArgumentParser


def find_if_used(all_gates, find_gate, operation):
    found = False
    for gate in all_gates:
        x, op, y, z = gate.replace(" ->", " ").split()
        if op == operation:
            if x == find_gate or y == find_gate:
                found = True
    return found


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        states, logic = file.read().split("\n\n")
    gates = logic.splitlines()

    faulty_gates = []
    for line in gates:
        x, op, y, z = line.replace(" ->", " ").split()

        # this is heavily inspired by online posts..
        if z.startswith("z") and op != "XOR":
            if not z[1:] == "45":
                print("1. faulty gate", z)
                faulty_gates.append(z)

        elif not z.startswith("z"):
            if not x.startswith("x") and not y.startswith("y"):
                if not x.startswith("y") and not y.startswith("x"):
                    if op not in ["AND", "OR"]:
                        print("2. faulty gate", z)
                        faulty_gates.append(z)

        if op == "XOR":
            if (
                x.startswith("x")
                and y.startswith("y")
                or x.startswith("y")
                and y.startswith("x")
            ):
                if not x[1:] == "00" or not y[1:] == "00":
                    if not find_if_used(gates, z, "XOR"):
                        print("3. faulty gate", z)
                        faulty_gates.append(z)

        elif op == "AND":
            if not x[1:] == "00" or not y[1:] == "00":
                if not find_if_used(gates, z, "OR"):
                    print("4. faulty gate", z)
                    faulty_gates.append(z)

    faulty_gates = sorted(list(set(faulty_gates)))
    print(",".join(i for i in faulty_gates))


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
