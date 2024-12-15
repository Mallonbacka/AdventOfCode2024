class Floor():
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.cells = [[None for x in range(width)] for y in range(height)] 

    def place(self, item):
        self.cells[item.y][item.x] = item

    def contents(self, x, y):
        return(self.cells[y][x])

    def empty_cell(self, x, y):
        self.cells[y][x] = None

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.contents(x, y), Wall):
                    print("#", end='')
                elif isinstance(self.contents(x, y), Box):
                    print("O", end='')
                elif isinstance(self.contents(x, y), Robot):
                    print("@", end='')
                else:
                    print(".", end='')
            print('')
        print('')

class GridObject():
    def __init__(self, x, y, floor):
        self.x = x
        self.y = y
        self.floor = floor

class MovingGridObject(GridObject):
    def move(self, command):
        self.floor.empty_cell(self.x, self.y)
        target_y = self.y
        target_x = self.x
        match command:
            case "^":
                target_y -= 1
            case ">":
                target_x += 1
            case "<":
                target_x -= 1
            case "v":
                target_y += 1
        if(self.floor.contents(target_x, target_y) == None or self.floor.contents(target_x, target_y).push(command)):
            self.x = target_x
            self.y = target_y
            self.floor.place(self)
            return True
        else:
            self.floor.place(self)
            return False

class Wall(GridObject):
    def push(self, _command):
        return False

class Box(MovingGridObject):
    def push(self, command):
        return self.move(command)

    def gps_value(self):
        return (100 * self.y) + self.x

class Robot(MovingGridObject):
    def push(self, command):
        raise 

with open("input.txt") as f:
    lines = f.readlines()

grid = []
instructions = ""
for line in lines:
    if(line.startswith("#")):
        grid.append(line.strip())
    elif(line.strip() != ""):
        instructions += line.strip()

floor = Floor(len(grid[0]), len(grid))
robot = None
boxes = []
for y in range(len(grid)):
    for x in range(len(grid[0])):
        match grid[y][x]:
            case "#":
                floor.place(Wall(x, y, floor))
            case "O":
                box = Box(x, y, floor)
                boxes.append(box)
                floor.place(box)
            case "@":
                robot = Robot(x, y, floor)
                floor.place(robot)

for command in instructions:
    robot.move(command)

print(sum(map(lambda x: x.gps_value(), boxes)))