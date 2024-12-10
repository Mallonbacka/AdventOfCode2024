def main():
    with open("input.txt") as f:
        lines = f.readlines()
    cells = format_values(lines)
    starts = trailheads(cells)
    print(sum(map(lambda x: search(x, cells), starts)))
    
def trailheads(lines):
    current = []
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if(lines[y][x] == 0):
                current.append((x, y))
    return current
        
def format_values(strings):
    return [list(map(lambda x: int(x), [*string.strip()])) for string in strings]

def search(start, cells):
    # Search for the cells allowed after level, starting from start
    # Return a 1 if the cell is a 9, 0 if it can't proceed, and the
    # sum of the routes in all other cases

    if(cells[start[1]][start[0]] == 9):
        return([(start[1], start[0])])
    
    neighbors = [(start[0] + 1, start[1]), 
                 (start[0] - 1, start[1]), 
                 (start[0], start[1] + 1), 
                 (start[0], start[1] - 1)]

    neighbors = [x for x in neighbors if x[0] >= 0 and x[0] < len(cells[0]) and x[1] >= 0 and x[1] < len(cells)]
    incrementing_neighbors = [x for x in neighbors if cells[x[1]][x[0]] == cells[start[1]][start[0]] + 1]

    return_value = []
    for neighbor in incrementing_neighbors:
        for result in search(neighbor, cells):
            return_value.append(result)

    if(cells[start[1]][start[0]] == 0):
        return len(return_value)
    else:
        return return_value


main()