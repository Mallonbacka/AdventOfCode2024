from collections import deque
from itertools import groupby

processed_cells = set()
areas = []
with open("input.txt") as f:
    cells = f.readlines()
rows = len(cells)
cols = len(cells[0]) - 1

nextDirection = {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N",
}
def main():
    for i in range(rows):
        for j in range(cols):
            process_cell(j, i)
    print(sum(map(lambda x: len(x) * count_corners(x), areas)))
    
    
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
    
def count_corners(area):
    corners = 0
    for cell in area:
        # check above
        current_value = cells[cell[1]][cell[0]]
        # Up and left
        if value_above(cell) != current_value and value_left(cell) != current_value:
            # Convex corner
            corners += 1
        elif value_above(cell) == current_value and value_left(cell) == current_value and value_up_left(cell) != current_value:
            # Concave corner
            corners += 1
        # Up and right
        if value_above(cell) != current_value and value_right(cell) != current_value:
            # Convex corner
            corners += 1
        elif value_above(cell) == current_value and value_right(cell) == current_value and value_up_right(cell) != current_value:
            # Concave corner
            corners += 1
        # Down and left
        if value_below(cell) != current_value and value_left(cell) != current_value:
            # Convex corner
            corners += 1
        elif value_below(cell) == current_value and value_left(cell) == current_value and value_down_left(cell) != current_value:
            # Concave corner
            corners += 1
        # Down and right
        if value_below(cell) != current_value and value_right(cell) != current_value:
            # Convex corner
            corners += 1
        elif value_below(cell) == current_value and value_right(cell) == current_value and value_down_right(cell) != current_value:
            # Concave corner
            corners += 1
    return corners



def value_above(cell):
    if cell[1] < 1:
        return None
    return cells[cell[1] - 1][cell[0]]

def value_left(cell):
    if cell[0] < 1:
        return None
    return cells[cell[1]][cell[0] - 1]

def value_up_left(cell):
    if cell[0] < 1 or cell[1] < 1:
        return None
    return cells[cell[1] - 1][cell[0] - 1]

def value_right(cell):
    if cell[0] >= cols - 1:
        return None
    return cells[cell[1]][cell[0] + 1]

def value_up_right(cell):
    if cell[0] >= cols or cell[1] < 1:
        return None
    return cells[cell[1] - 1][cell[0] + 1]

def value_below(cell):
    if cell[1] >= rows - 1:
        return None
    return cells[cell[1] + 1][cell[0]]

def value_down_left(cell):
    if cell[0] < 1 or cell[1] > rows:
        return None
    return cells[cell[1] + 1][cell[0] - 1]

def value_down_right(cell):
    if cell[0] >= cols or cell[1] > rows:
        return None
    return cells[cell[1] + 1][cell[0] + 1]

""" 
Dead code, left here for future inspiration?

def combine_edges(edges):
    turns = 0
    working_edges = list(edges)
    # Pick a good start point
    while(working_edges):
        starting = working_edges[0]
        current = nextPiece(starting, working_edges)
        while(current != starting):
            working_edges.remove(current)
            previous = current
            current = nextPiece(current, working_edges)
            #print(current)
            if(turned_corner(previous, current)):
                print("cornrer at", current[0], "between", current[1], "and", previous[1]) 
                print(previous, current)
                turns += 1 
        print(starting)
        working_edges.remove(starting)
    print("total corners", turns)
    return turns

def nextPiece(current, remaining):
    if current[0][0] == current[1][0] and current[0][1] == current[1][1] + 1:
        # x-coordinates match, border is on the north side, search for a north or east edge?
        if ((current[0][0] + 1, current[0][1]), (current[1][0] + 1, current[1][1])) in remaining:
            return ((current[0][0] + 1, current[0][1]), (current[1][0] + 1, current[1][1]))
        elif ((current[0][0], current[0][1]), (current[1][0] + 1, current[1][1] + 1)) in remaining:
            return ((current[0][0], current[0][1]), (current[1][0] + 1, current[1][1] + 1))
        elif ((current[0][0] + 1, current[0][1] - 1), (current[1][0], current[1][1])):
            return ((current[0][0] + 1, current[0][1] - 1), (current[1][0], current[1][1]))
        else:
            raise
    elif current[0][0] == current[1][0] and current[0][1] == current[1][1] - 1:
        # x-coordinates match, border is on the south side, search for a north or west edge?
        if ((current[0][0] - 1, current[0][1]), (current[1][0] - 1, current[1][1])) in remaining:
            return ((current[0][0] - 1, current[0][1]), (current[1][0] - 1, current[1][1]))
        elif ((current[0][0], current[0][1]), (current[1][0] - 1, current[1][1] - 1)) in remaining:
            return ((current[0][0], current[0][1]), (current[1][0] - 1, current[1][1] - 1))
        elif ((current[0][0] - 1, current[0][1] + 1), (current[1][0], current[1][1])):
            return ((current[0][0] - 1, current[0][1] + 1), (current[1][0], current[1][1]))
        else:
            raise
    elif current[0][0] == current[1][0] - 1 and current[0][1] == current[1][1]:
        # y-coordinates match, border is on the east
        if ((current[0][0], current[0][1] + 1), (current[1][0], current[1][1] + 1)) in remaining:
            return ((current[0][0], current[0][1] + 1), (current[1][0], current[1][1] + 1))
        elif ((current[0][0], current[0][1]), (current[1][0] - 1, current[1][1] + 1)) in remaining:
            return ((current[0][0], current[0][1]), (current[1][0] - 1, current[1][1] + 1))
        elif ((current[0][0] + 1, current[0][1] + 1), (current[1][0], current[1][1])):
            return ((current[0][0] + 1, current[0][1] + 1), (current[1][0], current[1][1]))
        else:
            raise
    elif current[0][0] == current[1][0] + 1 and current[0][1] == current[1][1]:
        # y-coordinates match, border is on the west 
        if ((current[0][0], current[0][1] - 1), (current[1][0], current[1][1] - 1)) in remaining:
            return ((current[0][0], current[0][1] - 1), (current[1][0], current[1][1] - 1))
        elif ((current[0][0], current[0][1]), (current[1][0] + 1, current[1][1] - 1)) in remaining:
            return ((current[0][0], current[0][1]), (current[1][0] + 1, current[1][1] - 1))
        elif ((current[0][0] - 1, current[0][1] - 1), (current[1][0], current[1][1])):
            return ((current[0][0] - 1, current[0][1] - 1), (current[1][0], current[1][1]))
        else:
            raise

def turned_corner(previous, current):
    if previous[0] == current[0]:
        return True
    if ((abs(current[0][0] - previous[0][0]) == 1) and (current[0][1] - previous[0][1] == 0)) or ((abs(current[0][1] - previous[0][1]) == 1) and (current[0][0] - previous[0][0] == 0)):
        return False
    return True

def outside_edges(cell):
    edges = []
    if(cell[0] == 0):
        edges.append((cell, (cell[0] - 1, cell[1])))
    if(cell[1] == 0):
        edges.append((cell, (cell[0], cell[1] - 1)))
    if(cell[0] == (cols - 1)):
        edges.append((cell, (cell[0] + 1, cell[1])))
    if(cell[1] == (rows - 1)):
        edges.append((cell, (cell[0], cell[1] + 1)))
    return edges

def interface_edges(cell):
    return list(map(lambda x: x, filter(lambda x: cells[cell[1]][cell[0]] != cells[x[1][1]][x[1][0]], neighbors_with_directions(cell[0], cell[1]))))

def neighbors(x, y):
    neighbors = [(x + 1, y), 
                 (x - 1, y), 
                 (x, y + 1), 
                 (x, y - 1)]

    return [x for x in neighbors if x[0] >= 0 and x[0] < cols and x[1] >= 0 and x[1] < rows]

def neighbors_with_directions(x, y):
    neighbors = [((x, y), (x + 1, y)), 
                 ((x, y), (x - 1, y)), 
                 ((x, y), (x, y + 1)), 
                 ((x, y), (x, y - 1))]

    return [x for x in neighbors if x[1][0] >= 0 and x[1][0] < cols and x[1][1] >= 0 and x[1][1] < rows] """

main()