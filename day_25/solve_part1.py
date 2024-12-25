from itertools import product


class Lock():
    def __init__(self, data):
        split_strings = data.split("\n")
        transposed_data = [[split_strings[j][i] for j in range(len(split_strings))] for i in range(len(split_strings[0]))]
        self.pin_heights = []
        for line in transposed_data:
            self.pin_heights.append(line.count("#") - 1)

    def as_list(self):
        return list(self.pin_heights)

    def __str__(self):
        return(str(self.pin_heights))

class Key():
    def __init__(self, data):
        split_strings = data.split("\n")
        transposed_data = [[split_strings[j][i] for j in range(len(split_strings))] for i in range(len(split_strings[0]))]
        reversed_strings = list(map(lambda x: x[::-1], transposed_data))
        self.pin_heights = []
        for line in reversed_strings:
            self.pin_heights.append(line.count("#") - 1)

    def as_list(self):
        return list(self.pin_heights)

    def __str__(self):
        return(str(self.pin_heights))

with open("input.txt") as f:
    content = f.read()

locks = []
keys = []

for item in content.split("\n\n"):
    if item.startswith("#"):
        locks.append(Lock(item))
    elif item.startswith("."):
        keys.append(Key(item))

count = 0

for lock, key in product(locks, keys):
    fits = True
    for i, column in enumerate(key.as_list()):
        if column + lock.as_list()[i] > 5:
            fits = False
            break
    if fits:
        count += 1

print(count)