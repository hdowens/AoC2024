from pathlib import Path


def part1(disk_map) -> None:
    #left most and right most incrementers
    lhs, rhs = 0, len(disk_map) - 1
    while lhs < rhs:
        while disk_map[lhs] != ".":
            #move pointer to the next element when its not a free space
            lhs += 1
        while disk_map[rhs] == ".":
            #move pointer to the next element when its a free space
            rhs -= 1
        if lhs < rhs:
            #do the swaperoo and move da pointers in their respective directions
            disk_map[lhs], disk_map[rhs] = disk_map[rhs], disk_map[lhs]
            lhs += 1
            rhs -= 1

    return sum(idx * int(i) for idx, i in enumerate(disk_map) if i != ".")
    
def get_empty_spaces(disk_map):
    empty_spaces = set()
    inc = 0
    while inc < len(disk_map):
        if disk_map[inc] == ".":
            j = inc
            while j < len(disk_map) and disk_map[j] == ".":
                j += 1
            empty_spaces.add((inc, j - inc))
            inc = inc + (j - inc) + 1
        else:
            inc += 1 
    return sorted(empty_spaces)

def part2(disk_map) -> None:
    
    empty_spaces = get_empty_spaces(disk_map)

    #now going to iterate through the chunks of data, chunk them and shove them into the first available empty space
    inc = len(disk_map) - 1
    already_moved = set()
    while inc >= 0:
        if disk_map[inc] != '.':
            cur_chunk = []
            j = inc
            while disk_map[j] == disk_map[inc]:
                cur_chunk.append(disk_map[j])   
                j -= 1
            
            #see if this has already tried to be moved:
            if tuple((j+1, inc, cur_chunk[0])) not in already_moved:

                #now we have our chunk, we need to find the first empty space that can fit it
                for start, length in sorted(empty_spaces):
                    if len(cur_chunk) <= length and start <= j:
                        #do the swaperoo
                        disk_map[start:start+len(cur_chunk)] = cur_chunk
                        disk_map[j+1:inc+1] = ['.'] * (inc - j)

                        #add it to already moved so once it is it doesnt constantly try and re-move it
                        already_moved.add(tuple((start, start+len(cur_chunk)-1, cur_chunk[0])))


                        if len(cur_chunk) != length:
                            #here we have the scenario where only part of the full space was used
                            #so we need to add the remaining space to the empty spaces
                            empty_spaces.append(
                                (start + len(cur_chunk), length - len(cur_chunk))
                            )

                        empty_spaces.remove((start, length)) 
                        #print(''.join(disk_map))
                        break

            inc = j
        else:
            inc -= 1

    return sum(idx * int(i) for idx, i in enumerate(disk_map) if i != ".")


def main() -> None:
    p = Path("puz_input.txt")
    with open(p.resolve(), "r") as input:
        disk_map = input.readline().strip()

    block_files_sizes = [disk_map[i] for i in range(0, len(disk_map), 2)]
    free_space_sizes  = [disk_map[i] for i in range(1, len(disk_map), 2)]

    disk_map = []
    for idx, num in enumerate(block_files_sizes):
        disk_map.extend([str(idx)] * int(block_files_sizes[idx]))
        if idx != len(block_files_sizes) - 1:
            disk_map.extend(["."] * int(free_space_sizes[idx]))

    print(f"Part 1: {part1(disk_map.copy())}")
    print(f"Part 2: {part2(disk_map)}")
    
    #print(''.join(disk_map))
    #go through the map and find all empty spaces and their start and lengths
   
if __name__ == "__main__":
    main()
