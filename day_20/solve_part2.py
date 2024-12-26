import copy
from heapq import heapify, heappop, heappush
from functools import cache

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Maze:
    def __init__(self, lines):
        self.width = len(lines[0].strip())
        self.height = len(lines)
        self.grid = [[None for x in range(self.width)] for y in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                match lines[y][x]:
                    case "#":
                        self.grid[y][x] = False
                    case ".":
                        self.grid[y][x] = True
                    case "S":
                        self.grid[y][x] = True
                        self.start = (x, y)
                    case "E":
                        self.grid[y][x] = True
                        self.end = (x, y)
    
    def is_passable(self, x, y):
        return self.grid[y][x] 

    def neighbors(self, point):
        cells = [(point[0] + d[0], point[1] + d[1]) for d in DIRECTIONS]
        return [cell for cell in cells if cell[0] >= 0 and cell[0] < self.width and cell[1] >= 0 and cell[1] < self.height]

    @cache
    def as_adjacency_list(self):
        tree = {}
        for y in range(self.height):
            for x in range(self.width):
                if self.is_passable(x, y):
                    tree[(x, y)] = []
                    for neighbor in self.neighbors((x, y)):
                        if self.is_passable(*neighbor):
                            tree[(x, y)].append(neighbor)
        return tree

    @cache
    def shortest_path_length(self):
        graph = self.as_adjacency_list()
        self.distances = {node: float("inf") for node in graph}
        self.distances[self.start] = 0

        pq = [(0, self.start)]
        heapify(pq)

        visited = set()

        while pq:
            current_distance, current_node = heappop(pq)
            if(current_node) in visited:
                continue
            visited.add(current_node)

            for next_state in graph[current_node]:
                new_distance = current_distance + 1
                if new_distance < self.distances[next_state]:
                    self.distances[next_state] = new_distance
                    heappush(pq, (new_distance, next_state))
            
        return self.distances[self.end]

    @cache
    def backtracked_path(self):
        graph = self.as_adjacency_list()
        predecessors = {node: None for node in graph}

        for node, distance in self.distances.items():
            for neighbor in graph[node]:
                if self.distances[neighbor] == distance + 1:
                    predecessors[neighbor] = node

        path = []
        current_node = self.end

        while current_node:
            path.append(current_node)
            current_node = predecessors[current_node]

        path.reverse()

        return enumerate(path)

    # Return tuple of (from, to)
    def possible_cheats(self):
        results = []
        for _step_id, point in self.backtracked_path():
            for neighbor in self.circle(point):
                if self.manhattan_distance(point, neighbor) <= 20:
                    results.append((point, neighbor))
        return results

    # Return tuple of (from, to, time saved)
    def allowed_cheats(self):
        results = []
        for cheat_from, cheat_to in self.possible_cheats():
            start_dist = self.distances.get(cheat_from, None)
            end_dist = self.distances.get(cheat_to, None)
            if start_dist != None and end_dist != None and start_dist < end_dist:
                new_total_time = start_dist + self.manhattan_distance(cheat_from, cheat_to) + (self.shortest_path_length() - end_dist)
                saving = self.shortest_path_length() - new_total_time
                if saving > 0:
                    results.append((cheat_from, cheat_to, saving))
        return results

    @cache
    def manhattan_distance(self, point_from, point_to):
        return abs(point_from[0] - point_to[0]) + abs(point_from[1] - point_to[1])

    @cache
    def circle(self, point):
       return [(x, y) for x in range(point[0] - 20, point[0] + 21) for y in range(point[1] - 20, point[1] + 21)]

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.start == (x, y):
                    print(".S.", end="")
                elif self.end == (x, y):
                    print(".E.", end="")
                elif self.is_passable(x, y):
                    print(str(self.distances[(x, y)]).zfill(3), end="")
                else:
                    print("###", end="")
            print("")

        
with open("input.txt") as f:
    lines = f.readlines()

maze = Maze(lines)
shortest_base_path = maze.shortest_path_length()

print(len(list(filter(lambda x: x[2] >= 100, maze.allowed_cheats()))))
