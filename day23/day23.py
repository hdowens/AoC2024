from pathlib import Path
from argparse import ArgumentParser
from collections import defaultdict
from itertools import combinations
import networkx as nx


def input_to_graph(data):
    G = nx.Graph()
    N = defaultdict(set)
    for line in data:
        n = line.split("-")
        N[n[0]].add(n[1])
        N[n[1]].add(n[0])
        G.add_edge(n[0], n[1])
    return N, G


def part1(com_dict: dict):
    triples = set()
    for key, item in com_dict.items():
        pairs = list(combinations(item, 2))
        for pair in pairs:
            if pair[0] in com_dict[pair[1]] and pair[1] in com_dict[pair[0]]:
                # Create a frozenset to avoid the TypeError
                triple = frozenset([key, pair[0], pair[1]])
                if triple not in triples:
                    triples.add(triple)

    chief_count = 0
    for s in triples:
        s = list(s)
        if s[0][0] == "t" or s[1][0] == "t" or s[2][0] == "t":
            chief_count += 1

    return chief_count, triples


def main(file_path: Path) -> None:
    with open(file_path, "r") as file:
        data = file.read().splitlines()

    lhs_computs = set(i.split("-")[0] for i in data)
    rhs_computs = set(i.split("-")[1] for i in data)

    computers = lhs_computs | rhs_computs
    com_dict = defaultdict(set)
    for com in computers:
        lhs_linked = set(i.split("-")[0] for i in data if i.split("-")[1] == com)
        rhs_linked = set(i.split("-")[1] for i in data if i.split("-")[0] == com)

        linked_computers = lhs_linked | rhs_linked
        com_dict[com] = linked_computers

    p1_ans, triples = part1(com_dict)
    print(f"Part 1: {p1_ans}")

    _, graph = input_to_graph(data)
    # here there is an algorithm that does this, I should research it
    max_clique = max([sorted(clique) for clique in nx.find_cliques(graph)], key=len)
    print(",".join(max_clique))


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
