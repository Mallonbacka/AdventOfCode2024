from collections import deque

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
def neighbors(coordinates):
    cells = [(coordinates[0] + d[0], coordinates[1] + d[1]) for d in directions]
    return [cell for cell in cells if cell[0] >= 0 and cell[0] < width and cell[1] >= 0 and cell[1] < height]

with open("input.txt") as f:
    lines = f.readlines()

start_x, start_y, end_x, end_y = [None, None, None, None]
is_open = {}

height = len(lines)
width = len(lines[0].strip())

for y, line in enumerate(lines):
    for x, cell in enumerate(line):
        match cell:
            case "#":
                is_open[(x, y)] = False 
            case "S":
                start_x, start_y = x, y
                is_open[(x, y)] = True 
            case "E":
                end_x, end_y = x, y
                is_open[(x, y)] = True 
            case ".":
                is_open[(x, y)] = True 

initial_is_open = is_open.copy()

def shortest_path_and_distance():
    local_is_open = initial_is_open.copy()

    # Convert grid to graph
    tree = {}
    for y in range(height):
        for x in range(width):
            if local_is_open[(x, y)]:
                tree[(x, y)] = []
                for neighbor in neighbors((x, y)):
                    if local_is_open[neighbor]:
                        tree[(x, y)].append(neighbor)

    # Simple BFS
    visited = []
    queue = deque([(0, (start_x, start_y), None)])
    distances = { node: float("inf") for node in tree.keys()}
    predecessors = {}

    while queue:
        current_distance, node, predecessor = queue.popleft()

        if node not in visited:
            visited.append(node)
            if current_distance < distances[node]:
                distances[node] = current_distance
                predecessors[node] = predecessor

            for neighbor in tree[node]:
                if neighbor not in visited:
                    queue.append((current_distance + 1, neighbor, node))
            
            if node == (end_x, end_y):
                break
    
    # backtrack
    backtracking_node = (end_x, end_y)
    path = [backtracking_node]
    while(backtracking_node != (start_x, start_y)):
        new_node = predecessors[backtracking_node]
        path.append(new_node)
        backtracking_node = new_node
    
    return (path, distances[(end_x, end_y)])

def shortest_distance_after_removal(cell):
    local_is_open = initial_is_open.copy()
    if cell:
        local_is_open[cell] = True

    # Convert grid to graph
    tree = {}
    for y in range(height):
        for x in range(width):
            if local_is_open[(x, y)]:
                tree[(x, y)] = []
                for neighbor in neighbors((x, y)):
                    if local_is_open[neighbor]:
                        tree[(x, y)].append(neighbor)

    # Simple BFS
    visited = []
    queue = deque([(0, (start_x, start_y))])
    distances = { node: float("inf") for node in tree.keys()}

    while queue:
        current_distance, node = queue.popleft()

        if node not in visited:
            visited.append(node)
            if current_distance < distances[node]:
                distances[node] = current_distance

            for neighbor in tree[node]:
                if neighbor not in visited:
                    queue.append((current_distance + 1, neighbor))
            
            if node == (end_x, end_y):
                break
    
    return distances[(end_x, end_y)]

path, original_distance = shortest_path_and_distance()
counter = 0

def open_two_sides(point):
    return (initial_is_open[(point[0] + 1, point[1])] and initial_is_open[(point[0] - 1, point[1])]) or (initial_is_open[(point[0], point[1] - 1)] and initial_is_open[(point[0], point[1] + 1)]) 

path_neighbors = set([])

for a in map(lambda x: neighbors(x), path):
    for b in a:
        path_neighbors.add(b)

print(len(path_neighbors))

def close_to_path(point):
    return point in path_neighbors

interior_walls = [x for x in is_open if x[0] > 0 and x[1] > 0 and x[0] < width - 1 and x[1] < height - 1]
removable_walls = [x for x in interior_walls if open_two_sides(x) and close_to_path(x)]

print(len(removable_walls))
for wall in removable_walls:
    print(wall)
    shortest_distance = shortest_distance_after_removal(wall)
    if(original_distance - shortest_distance >= 100):
        counter += 1
    
print(counter)