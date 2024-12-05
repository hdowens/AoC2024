from pathlib import Path


def part1(rules, instructions) -> None:
    total = 0
    for idx, it in enumerate(instructions):        
        err_flag = True
        for i in range(0, len(it)):
            #print(f"Testing element [{it[i]}]")
            for j in range(i+1, len(it)):
                #print(f"\tF: [{it[j]}|{it[i]}] must not exist")
                if (it[j], it[i]) in rules and err_flag:
                    #print(f"\tF [{idx}] failed because {(it[j], it[i])} exists")
                    err_flag = False
            #for k in range(i, -1, -1):
            #    if it[i] != it[k]:
            #        if (it[i], it[k]) in rules and err_flag:
            #        #print(f"\tB: [{it[i]}|{it[k]}] must not exist")
            #            print(f"\tB [{idx}] failed because {(it[i], it[k])} exists")
            #            err_flag = False

        if err_flag:
            #print(f"\t[{idx}] {it} is correct")
            total += it[(len(it)-1) // 2]

    return total

def part2(rules, instructions) -> None:
    new_insrts = []
    for idx, it in enumerate(instructions):
        err_flag = True        
        for i in range(0, len(it)):
            for j in range(i+1, len(it)):
                if (it[j], it[i]) in rules:
                    err_flag = False
                    #print(f"F [{idx}] failed because {(it[j], it[i])} exists")
                    it[j], it[i] = it[i], it[j]
        
        if not err_flag:
            new_insrts.append(it)


    return sum(it[(len(it)-1) // 2] for it in new_insrts)



def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().split("\n\n")

    #lets transform the rules into a list of tuples
    rules = [tuple(map(int, s.split("|"))) for s in data[0].split("\n")]

    #lets transform the instructions into a list of list of integers    
    instructions = [list(map(int, sample.split(','))) for sample in data[1].split("\n")]

    print(f"Part 1: {part1(rules, instructions)}")
    print(f"Part 2: {part2(rules, instructions)}")


if __name__ == "__main__":
    main()


