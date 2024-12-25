from functools import reduce
import itertools

ACTIONS = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}

def shortest_sequences(all_sequences):
    min_length = min(map(len, all_sequences))
    shortest_seqs = filter(lambda x: len(x) == min_length, all_sequences)
    return set(shortest_seqs)

class Keypad():
    def __init__(self):
        self.current_button = 'A'

    def move_to_with_all_shortest_routes(self, destination_button):
        diff = self.diff_to(destination_button)
        steps = []
        if diff[0] < 0:
            steps.extend(['<' for x in range(-diff[0])])
        else:
            steps.extend(['>' for x in range(diff[0])])
        if diff[1] < 0:
            steps.extend(['^' for x in range(-diff[1])])
        else:
            steps.extend(['v' for x in range(diff[1])])
        results = list(set(itertools.permutations(steps)))
        results = list(map(lambda x: ''.join(x), filter(self.is_allowed, results)))
        self.current_button = destination_button
        return results

    def press_sequences(self, keys):
        return set(map(lambda x: 'A'.join(x) + 'A', itertools.product(*map(lambda x: self.move_to_with_all_shortest_routes(x), keys))))

    def all_shortest_press_sequences(self, seqs):
        results = []
        for sequence in seqs:
            results.extend(self.press_sequences(sequence))
        return shortest_sequences(results)

    def buttons(self):
        return self.buttons_with_coordinates().keys()

    def manhattan_distance_to(self, button):
        current = self.buttons_with_coordinates()[self.current_button]
        destination = self.buttons_with_coordinates()[button]
        return abs(current[0] - destination[0]) + abs(current[1] - destination[1])

    def diff_to(self, button):
        current = self.buttons_with_coordinates()[self.current_button]
        destination = self.buttons_with_coordinates()[button]
        return (destination[0] - current[0], destination[1] - current[1])
    
    def is_allowed(self, sequence):
        cells = []
        location = self.buttons_with_coordinates()[self.current_button]
        for step in sequence:
            cells.append(location)
            location = (location[0] + ACTIONS[step][0], location[1] + ACTIONS[step][1])
        return not any(map(lambda x: x in self.disallowed_cells(), cells))

class NumericKeypad(Keypad):
    def buttons_with_coordinates(self):
        return {
            '1': (0, 2),
            '2': (1, 2),
            '3': (2, 2),
            '4': (0, 1),
            '5': (1, 1),
            '6': (2, 1),
            '7': (0, 0),
            '8': (1, 0),
            '9': (2, 0),
            '0': (1, 3),
            'A': (2, 3),
        }

    def disallowed_cells(self):
        return [(0,3)]
    
class DirectionalKeypad(Keypad):
    def buttons_with_coordinates(self):
        return {
            '^': (1, 0),
            'A': (2, 0),
            '<': (0, 1),
            'v': (1, 1),
            '>': (2, 1),
        }

    def disallowed_cells(self):
        return [(0,0)]

with open("input.txt") as f:
    lines = f.readlines()

sum = 0
for line in lines:
    numpad = NumericKeypad()
    robot1_dirpad = DirectionalKeypad()
    my_dirpad = DirectionalKeypad()

    numeric_pad_options = shortest_sequences(numpad.press_sequences(line.strip()))

    robot1_options = robot1_dirpad.all_shortest_press_sequences(numeric_pad_options)
    robot2_options = my_dirpad.all_shortest_press_sequences(robot1_options)

    sum += len(list(robot2_options)[0]) * int(line.strip().replace("A", ''))

print(sum)
