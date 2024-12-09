from pathlib import Path
from itertools import combinations

def find_attena(data: list, char: str) -> str:
    ret = []
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == char:
                ret.append((x, y)) 
    return ret

def bounds_check(x: int, y: int, data: list) -> bool:
    return x >= 0 and y >= 0 and x < len(data) and y < len(data[0]) 

def part1(data, antennas):
    pp_data = [list(line) for line in data]
    antinodes_placed = set()
    for antenna in antennas:
        alst = find_attena(data, antenna)
        
        for previous, current in list(combinations(alst, 2)):
            dx, dy = current[0] - previous[0] , current[1] - previous[1]   

            an_1 = (previous[0] + (-dx), previous[1] + (-dy))
            an_2 = (current[0] + dx, current[1] + dy)
            print(f"{previous} -> {an_1}\n{current} -> {an_2}\n\t dx: {dx} dy: {dy}")

            if bounds_check(an_1[0], an_1[1], pp_data):
                if pp_data[an_1[0]][an_1[1]] != antenna:    
                    antinodes_placed.add(an_1)
                    if pp_data[an_1[0]][an_1[1]] == '.':
                        pp_data[an_1[0]][an_1[1]] = '#'
            
            if bounds_check(an_2[0], an_2[1], pp_data):
                if pp_data[an_2[0]][an_2[1]] != antenna :
                    antinodes_placed.add(an_2)
                    if pp_data[an_2[0]][an_2[1]] == '.':
                        pp_data[an_2[0]][an_2[1]] = '#'
            

    print('\n'.join([''.join(line) for line in pp_data]))
    return len(antinodes_placed)



def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        data = input.read().splitlines()

    antennas = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    #print(f"Part1: {part1(data, antennas)}")
    pp_data = [list(line) for line in data]
    antinode_count = 0
    antinodes_placed = set()
    for antenna in antennas:
        alst = find_attena(data, antenna)
        
        for previous, current in list(combinations(alst, 2)):
            dx, dy = current[0] - previous[0] , current[1] - previous[1]   
            an_1 = (previous[0] + (-dx), previous[1] + (-dy))
            an_2 = (current[0] + dx, current[1] + dy)
            print(f"{previous} -> {an_1}\n{current} -> {an_2}\n\t dx: {dx} dy: {dy}")   
            while bounds_check(an_1[0], an_1[1], pp_data) or bounds_check(an_2[0], an_2[1], pp_data):
                
                if bounds_check(an_1[0], an_1[1], pp_data):
                    if pp_data[an_1[0]][an_1[1]] != antenna:    
                        antinodes_placed.add(an_1)
                        if pp_data[an_1[0]][an_1[1]] == '.':
                            pp_data[an_1[0]][an_1[1]] = '#'
                
                if bounds_check(an_2[0], an_2[1], pp_data):
                    if pp_data[an_2[0]][an_2[1]] != antenna :
                        antinodes_placed.add(an_2)
                        if pp_data[an_2[0]][an_2[1]] == '.':
                            pp_data[an_2[0]][an_2[1]] = '#'

                previous, current = an_1, an_2
                an_1 = (previous[0] + (-dx), previous[1] + (-dy))
                an_2 = (current[0] + dx, current[1] + dy)



        for pos in alst:
            antinodes_placed.add(pos)


    print(len(antinodes_placed))



if __name__ == "__main__":
    main()
