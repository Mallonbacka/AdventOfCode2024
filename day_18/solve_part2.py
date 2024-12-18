from collections import deque

width = 71
height = 71

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
def neighbors(coordinates):
    cells = [(coordinates[0] + d[0], coordinates[1] + d[1]) for d in directions]
    return [cell for cell in cells if cell[0] >= 0 and cell[0] < width and cell[1] >= 0 and cell[1] < height]

with open("input.txt") as f:
    lines = f.readlines()

low = 1024
high = 3450

while low < (high - 1):
    midpoint = int((high + low) / 2)
    is_open = [ [True] * width for i in range(height) ]
    for line in lines[:midpoint]:
        corrupt = line.strip().split(",")
        is_open[int(corrupt[1])][int(corrupt[0])] = False

    # Convert grid to graph
    tree = {}
    for y in range(height):
        for x in range(width):
            if is_open[y][x]:
                tree[(x, y)] = []
                for neighbor in neighbors((x, y)):
                    if is_open[neighbor[1]][neighbor[0]]:
                        tree[(x, y)].append(neighbor)

    # Simple BFS
    visited = []
    queue = deque([(0, (0, 0))])
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

    if distances[(width - 1, height - 1)] < float("inf"):
        # Solution found, increase low
        low = midpoint
    else:
        # No solution found, decrease high
        high = midpoint

print(lines[low].strip())