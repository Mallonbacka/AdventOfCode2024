
import itertools


class Network():
    def __init__(self):
        self.relations = {}
        
    def add_connection(self, computer_1, computer_2):
        if not self.relations.get(computer_1):
            self.relations[computer_1] = {}
        self.relations[computer_1][computer_2] = True
        if not self.relations.get(computer_2):
            self.relations[computer_2] = {}
        self.relations[computer_2][computer_1] = True

    def groups(self):
        results = []
        for combination in itertools.combinations(self.computers(), 3):
            connected = True
            for pair in itertools.combinations(combination, 2):
                if not self.relations[pair[0]].get(pair[1]):
                    connected = False
            if connected:
                results.append(combination)
        return results

    def groups_starting(self, search):
        return list(filter(lambda x: any(map(lambda y: y.startswith(search), x)), self.groups()))

    def summary(self):
        return self.relations

    def computers(self):
        return self.relations.keys()
    
with open("input.txt") as f:
    lines = f.readlines()

network = Network()
for line in lines:
    network.add_connection(*line.strip().split("-"))

print(len(network.groups_starting('t')))