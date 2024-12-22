import math

class NumberGenerator():
    def __init__(self, starting_number):
        self.current_value = int(starting_number)

    def next_number(self):
        # Step 1
        self.current_value = NumberGenerator.prune(NumberGenerator.mix(self.current_value * 64, self.current_value))
        # Step 2
        self.current_value = NumberGenerator.prune(NumberGenerator.mix(math.floor(self.current_value / 32), self.current_value))
        # Step 3
        self.current_value = NumberGenerator.prune(NumberGenerator.mix(self.current_value * 2048, self.current_value))

        return self.current_value

    @classmethod
    def mix(cls, value1, value2):
        return value1 ^ value2

    @classmethod
    def prune(cls, value):
        return value % 16777216

    
with open("input.txt") as f:
    lines = f.readlines()

sum = 0

for line in lines:
    generator = NumberGenerator(int(line.strip()))

    for n in range(1999):
        generator.next_number()

    sum += generator.next_number()

print(sum)