import time
from collections import deque

processed_cells = set()
areas = []
with open("input.txt") as f:
    cells = f.readlines()
rows = len(cells)
cols = len(cells[0]) - 1

def main():
    for i in range(rows):
        for j in range(cols):
            process_cell(j, i)
    print(sum(map(lambda x: len(x) * get_perimeter(x), areas)))
    
    
def process_cell(x, y):
    if((x, y) in processed_cells):
        return
    areas.append(get_contiguous_area(x, y))

def get_contiguous_area(x, y):
    results = set([(x, y)])
    to_ignore = set()
    to_check = set([*neighbors(x, y)])
    # Test the neighbors
    while(to_check):
        check = to_check.pop()
        if(cells[check[1]][check[0]] == cells[y][x]):
            # Symbols match
            results.add(check)
            processed_cells.add(check)
            for neighbor in neighbors(check[0], check[1]):
                if(neighbor in results or neighbor in to_check or neighbor in to_ignore):
                    continue 
                to_check.add(neighbor)
        else:
            to_ignore.add(check)
    # Return this cell, plus the recursive results of the neighbors 
    return results
    
def get_perimeter(area):
    fence = 0
    for cell in area:
        # Interfaces with other cells
        fence += len(list(filter(lambda x: cells[cell[1]][cell[0]] != cells[x[1]][x[0]], neighbors(cell[0], cell[1]))))
        # External interfaces
        fence += outside_edges(cell)
    return fence

def outside_edges(cell):
    edges = 0
    if(cell[0] == 0):
        edges += 1
    if(cell[1] == 0):
        edges += 1
    if(cell[0] == (cols - 1)):
        edges += 1
    if(cell[1] == (rows - 1)):
        edges += 1
    return edges

def neighbors(x, y):
    neighbors = [(x + 1, y), 
                 (x - 1, y), 
                 (x, y + 1), 
                 (x, y - 1)]

    return [x for x in neighbors if x[0] >= 0 and x[0] < cols and x[1] >= 0 and x[1] < rows]

main()