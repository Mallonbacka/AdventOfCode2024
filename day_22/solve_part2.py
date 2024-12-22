import math

class NumberGenerator():
    def __init__(self, starting_number):
        self.current_value = int(starting_number)
        self.previous_value = None
        self.recent_changes = []

    def next_number(self):
        self.previous_value = self.current_value
        # Step 1
        self.current_value = NumberGenerator.prune(NumberGenerator.mix(self.current_value * 64, self.current_value))
        # Step 2
        self.current_value = NumberGenerator.prune(NumberGenerator.mix(math.floor(self.current_value / 32), self.current_value))
        # Step 3
        self.current_value = NumberGenerator.prune(NumberGenerator.mix(self.current_value * 2048, self.current_value))
        
        self.recent_changes.append(self.change_from_previous_last_digit())
        if len(self.recent_changes) > 4:
            self.recent_changes.pop(0)

        return self.current_value

    def last_digit(self):
        return self.current_value % 10

    def change_from_previous_last_digit(self):
        return self.last_digit() - (self.previous_value % 10)

    def last_four_changes(self):
        return self.recent_changes

    @classmethod
    def mix(cls, value1, value2):
        return value1 ^ value2

    @classmethod
    def prune(cls, value):
        return value % 16777216

    
generator = NumberGenerator(123)

with open("input.txt") as f:
    lines = f.readlines()

# Key = sequence of changes, value = dict with key = starting value, value = price 
results = {}

for line in lines:
    starting_value = int(line.strip())
    generator = NumberGenerator(starting_value)

    for n in range(3):
        # Nothing to save here
        generator.next_number()

    for n in range(1997):
        generator.next_number()
        current_price = generator.last_digit()
        sequence = ",".join(map(str, generator.last_four_changes()))
        if sequence not in results.keys():
            results[sequence] = {}
        if str(starting_value) not in results[sequence].keys():
            results[sequence][str(starting_value)] = current_price

totals = { sequence: sum(prices.values()) for sequence, prices in results.items() }
print(max(totals.values()))
# print(sum)