
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

    def computers(self):
        return self.relations.keys()

    def connections_per_computer(self):
        return { key: len(value.keys()) for key, value in self.relations.items() }

    # Based on https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    def bron_kerbosch(self, r, p, x):
        if len(p) == 0 and len(x) == 0:
            return(set([",".join(sorted(r))]))
        results = set([])
        for v in p:
            neighbors = self.relations[v].keys()
            for group in self.bron_kerbosch(r + [v], list(set(p) & neighbors), list(set(p) & neighbors)):
                results.add(group)
            p.remove(v)
            x.append(v)
        return results

    def find_biggest_network(self):
        all_groups = self.bron_kerbosch([], list(self.computers()), [])
        return max(all_groups, key=len)
    
with open("input.txt") as f:
    lines = f.readlines()

network = Network()
for line in lines:
    network.add_connection(*line.strip().split("-"))

print(network.find_biggest_network())