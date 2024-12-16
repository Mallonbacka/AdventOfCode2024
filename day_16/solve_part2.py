import time
from heapq import heapify, heappop, heappush

class Action:
    def __init__(self, x, y, symbol, points):
        self.dx = x
        self.dy = y
        self.symbol = symbol
        self.points = points

    def dx(self):
        return self.dx

    def dy(self):
        return self.dy

    def __str__(self):
        return self.symbol

POSSIBLE_MOVES = [
    Action(-1, 0, "<", 1),
    Action(0, 1, "v", 1000),
    Action(1, 0, ">", 1),
    Action(0, -1, "^", 1000),
]

DIRECTIONS = set(['^', '>', 'v', '<'])
OPPOSITE = { '^': 'v', '>': '<', '<': '>', 'v': '^' }
CHANGES = { '^': (0, -1), '>': (1, 0), '<': (-1, 0), 'v': (0, 1) }

class Route:
    def __init__(self, current_location, action, previous_locations, previous_steps):
        self.current_location = current_location
        self.action = action
        self.previous_locations = (previous_locations or [])
        self.previous_steps = previous_steps

    def new_location(self):
        return (self.current_location[0] + self.action.dx, self.current_location[1] + self.action.dy)
    
    def is_backwards(self):
        return self.new_location() in self.previous_locations

    def all_steps(self):
        return (self.previous_steps or "") + str(self.action)

    def all_locations(self):
        return self.previous_locations + [self.current_location]

    def all_steps_score(self):
        total = 0
        prev = '>'
        for step in self.all_steps():
            if step == prev:
                total += 1
            else:
                total += 1001
                prev = step
        return total

    def __str__(self):
        info = "Action " + str(self.current_location) + " " + str(self.action)
        if self.previous_locations:
            info += " (excluding " + str(self.previous_locations) + ")"
        return info

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[None for x in range(width)] for y in range(height)]
        
    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] == None:
                    print('.', end='')
                else:
                    print(self.data[y][x], end='')
            print('')

    def place_wall(self, x, y):
        self.place(Wall(), x, y)

    def place(self, thing, x, y):
        if isinstance(thing, StartPoint):
            self.start_x = x
            self.start_y = y
        elif isinstance(thing, EndPoint):
            self.end_x = x
            self.end_y = y
        self.data[y][x] = thing

    def get_cell(self, point):
        return self.data[point[1]][point[0]]

    def start_point(self):
        return((self.start_x, self.start_y, '>'))

    def end_points(self):
        return list(map(lambda x: (self.end_x, self.end_y, x), DIRECTIONS))

    def all_paths(self):
        paths_found = []
        actions_to_check = []
        
        for action in POSSIBLE_MOVES:
            new_route = Route((self.start_x, self.start_y), action, None, None)
            if not isinstance(self.get_cell(new_route.new_location()), Wall):
                actions_to_check.append(new_route)
        
        while(actions_to_check):
            action = actions_to_check.pop()
            for next_action in POSSIBLE_MOVES:
                next_route = Route(action.new_location(), next_action, action.all_locations(), action.all_steps())
                if isinstance(self.get_cell(next_route.new_location()), EndPoint):
                    paths_found.append(next_route)
                elif not isinstance(self.get_cell(next_route.new_location()), Wall) and not next_route.is_backwards():
                    actions_to_check.append(next_route)
        
        return list(map(lambda x: x.all_steps_score(), paths_found))

    def adjacency_list(self):
        nodes = {}
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if not isinstance(self.get_cell((x, y)), Wall):
                    for direction in DIRECTIONS:
                        current_key = (x, y, direction)
                        nodes[current_key] = {}
                        for destination in (DIRECTIONS - set([OPPOSITE[direction]])):
                            if destination == direction:
                                change = CHANGES[direction]
                                if not isinstance(self.get_cell((x + change[0], y + change[1])), Wall):
                                    nodes[current_key][(x + change[0], y + change[1], direction)] = 1
                            else:
                                nodes[current_key][(x, y, destination)] = 1000
        return nodes

class Wall:
    def __str__(self):
        return '#'

class StartPoint:
    def __str__(self):
        return 'S'

class EndPoint:
    def __str__(self):
        return 'E'

with open("input.txt") as f:
    lines = f.readlines()

width = len(lines[0].strip())
height = len(lines)
grid = Grid(width, height)
for y in range(height):
    for x in range(width):
        if lines[y][x] == "#":
            grid.place_wall(x, y)
        elif lines[y][x] == "S":
            grid.place(StartPoint(), x, y)
        elif lines[y][x] == "E":
            grid.place(EndPoint(), x, y)
        
# Solve
graph = grid.adjacency_list()
distances = {node: float("inf") for node in graph}
distances[grid.start_point()] = 0

pq = [(0, grid.start_point())]
heapify(pq)

visited = set()

while pq:
    current_distance, current_node = heappop(pq)
    if(current_node) in visited:
        continue
    visited.add(current_node)

    for next_state, weight in graph[current_node].items():
        new_distance = current_distance + weight
        if new_distance < distances[next_state]:
            distances[next_state] = new_distance
            heappush(pq, (new_distance, next_state))

min_score = min(map(lambda x: distances[x], grid.end_points()))

winning_end_points = list(filter(lambda x: distances[x] == min_score, grid.end_points()))

predecessors = {node: [] for node in graph}

for node, distance in distances.items():
   for neighbor, weight in graph[node].items():
       if distances[neighbor] == distance + weight:
           predecessors[neighbor] += [node]

all_tiles = []
for end_point in winning_end_points:
    path = []
    nodes_to_backtrack_from = [end_point]

    # Backtrack from the target node using predecessors
    while nodes_to_backtrack_from:
        current_node = nodes_to_backtrack_from.pop()
        path.append(current_node)
        for node in predecessors[current_node]:
            nodes_to_backtrack_from.append(node)

    # Reverse the path and return it
    all_tiles += path

print(len(set([ (x, y) for (x, y, z) in all_tiles ])))