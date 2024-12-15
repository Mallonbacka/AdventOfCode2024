class Floor():
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.cells = [[None for x in range(width)] for y in range(height)] 

    def place(self, item):
        self.cells[item.y][item.x] = item

    def contents(self, x, y):
        if self.cells[y][x] != None:
            return(self.cells[y][x])
        elif isinstance(self.cells[y][x - 1], Wall) or isinstance(self.cells[y][x - 1], Box):
            return(self.cells[y][x-1])

    def empty_cell(self, x, y):
        self.cells[y][x] = None

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.contents(x, y), Wall):
                    print("#", end='')
                elif isinstance(self.contents(x, y), Box):
                    if self.contents(x, y) == self.contents(x + 1, y):
                        print("[", end='')
                    else:
                        print("]", end='')
                elif isinstance(self.contents(x, y), Robot):
                    print("@", end='')
                else:
                    print(".", end='')
            print('')
        print('')

    def get_gps_total(self):
        gps_total = 0
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.cells[y][x], Box):
                    gps_total += (100 * y) + x
        return gps_total

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
        if(self.can_move(target_x, target_y, command) and self.push_or_empty(target_x, target_y, command)):
        #if(self.push_or_empty(target_x, target_y, command)):
            self.x = target_x
            self.y = target_y
            self.floor.place(self)
            return True
        else:
            self.floor.place(self)
            return False

    def push_or_empty(self, target_x, target_y, command):
        if(isinstance(self, Robot)):
            # Width is one, check one cell
            return self.floor.contents(target_x, target_y) == None or self.floor.contents(target_x, target_y).push(command)
        elif(isinstance(self, Box)):
            # Width is two, check two cells
            return (self.floor.contents(target_x, target_y) == None or self.floor.contents(target_x, target_y).push(command)) and (self.floor.contents(target_x + 1, target_y) == None or self.floor.contents(target_x + 1, target_y).push(command))

    def can_move(self, target_x, target_y, command):
        # Can the thing in target_x, target_y move?
        if(self.floor.contents(target_x, target_y) == None):
            return True
        elif isinstance(self.floor.contents(target_x, target_y), Wall):
            return False
        elif self.floor.contents(target_x, target_y) == self:
            return True
        elif isinstance(self.floor.contents(target_x, target_y), Box):
            next_target_x, next_target_y = target_x, target_y
            match command:
                case "^":
                    next_target_y -= 1
                case ">":
                    next_target_x += 1
                case "<":
                    next_target_x -= 1
                case "v":
                    next_target_y += 1
            if(self.floor.contents(target_x - 1, target_y) == self.floor.contents(target_x, target_y)):
                # This is the "secondary" box cell
                return self.floor.contents(target_x, target_y).can_move(next_target_x, next_target_y, command)
            else:
                # this is the "main" box cell
                return self.floor.contents(target_x, target_y).can_move(next_target_x, next_target_y, command) and self.floor.contents(target_x, target_y).can_move(next_target_x + 1, next_target_y, command)


class Wall(GridObject):
    def push(self, _command):
        return False

class Box(MovingGridObject):
    def push(self, command):
        #print("box receives push")
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

floor = Floor(len(grid[0]) * 2, len(grid))
robot = None
boxes = []
for y in range(len(grid)):
    for x in range(0, len(grid[0]) * 2, 2):
        match grid[y][int(x / 2)]:
            case "#":
                floor.place(Wall(x, y, floor))
            case "O":
                box = Box(x, y, floor)
                boxes.append(box)
                floor.place(box)
            case "@":
                robot = Robot(x, y, floor)
                floor.place(robot)

#floor.print()
for command in instructions:
    robot.move(command)
    #print("Move", command)
    #floor.print()
    #input()
#floor.print()

print(floor.get_gps_total())