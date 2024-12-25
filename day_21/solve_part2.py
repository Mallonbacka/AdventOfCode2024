from functools import reduce, cache
import itertools
import re

ACTIONS = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}

def cheapest(sequences):
    if(any([len(x) == 0 for x in sequences])):
        return ""
    return sorted(sequences, key=lambda x: changes(x))[0]

def changes(s1):
    counter = 0
    prev = s1[0]
    for char in s1[1:]:
        if char != prev:
            counter += 1
        prev = char
    return counter

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
        #results = [cheapest(results)]
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

    @cache
    def all_routes(self):
        all_routes = {}
        for start in self.buttons():
            all_routes[start] = {}
            for end in self.buttons():
                self.current_button = start
                all_routes[start][end] = list(self.move_to_with_all_shortest_routes(end))
        return all_routes

    @cache
    def build_sequence(self, keys, index, prevKey, current_path):
        result = []
        if index == len(keys):
            result.append(current_path)
            return result
        for path in self.all_routes()[prevKey][keys[index]]:
            result = result + self.build_sequence(keys, index + 1, keys[index], current_path + path + 'A')
        return result

    @cache
    def shortest(self, keys, depth):
        if depth == 0:
            return len(keys)
        total = 0
        groups = [x + "A" for x in keys.split("A")]
        groups[-1] = groups[-1].strip("A")
        for key_group in groups:
            seqs = self.build_sequence(key_group, 0, 'A', "")
            minimum = float("inf")
            for seq in seqs:
                if self.shortest(seq, depth - 1) < minimum:
                    minimum = self.shortest(seq, depth - 1)
            total += minimum
        return total


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
    dirpad = DirectionalKeypad()

    numpad_options = numpad.build_sequence(line.strip(), 0, "A", "")
    result = min([dirpad.shortest(x, 25) for x in numpad_options])

    sum += result * int(line.strip().replace("A", ''))

print(sum)
