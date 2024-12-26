from time import sleep


class Circuit():
    def __init__(self):
        self.wires = {}
        self.gates = {}
        self.evaluated_gates = {}
        self.direct_dependencies = {}

    def set_wire_value(self, wire, value):
        self.wires[wire] = bool(value)

    def add_gate(self, wire, left, operator, right):
        self.gates[wire] = (left, operator, right)
        if wire not in self.direct_dependencies.keys():
            self.direct_dependencies[wire] = set([])
        self.direct_dependencies[wire].add(left)
        self.direct_dependencies[wire].add(right)

    def all_dependencies(self, wire):
        results = set([])
        if wire not in self.direct_dependencies.keys():
            return results
        for dependency in self.direct_dependencies[wire]:
            results.add(dependency)
            for child in self.all_dependencies(dependency):
                results.add(child)
        return results

    def input_dependencies(self, wire):
        return set(filter(lambda x: x.startswith("x") or x.startswith("y"), self.all_dependencies(wire)))

    def all_wires(self):
        return self.wires | self.gates

    def has_value(self, wire):
        return wire in self.wires.keys() or wire in self.evaluated_gates.keys()
    
    def value(self, wire):
        if wire in self.wires.keys():
            return self.wires[wire] 
        elif wire in self.evaluated_gates.keys():
            return self.evaluated_gates[wire]
        else:
            raise KeyError

    def evaluate(self, wire):
        left, operator, right = self.gates[wire]
        match operator:
            case "AND":
                self.evaluated_gates[wire] = self.value(left) and self.value(right)
            case "OR":
                self.evaluated_gates[wire] = self.value(left) or self.value(right)
            case "XOR":
                self.evaluated_gates[wire] = self.value(left) != self.value(right)

    def evaluate_fully(self):
        unevaluated_gates = list(self.gates.keys()).copy()
        while unevaluated_gates:
            for wire in unevaluated_gates:
                gate = self.gates[wire]
                if self.has_value(gate[0]) and self.has_value(gate[2]):
                    self.evaluate(wire)
                    unevaluated_gates.remove(wire)
        return self.evaluated_gates

    def wires_value(self, group):
        total = 0
        column = 0
        while True:
            if not self.has_value(group + format(column, '02')):
                break
            value = 1 if self.value(group + format(column, '02')) else 0
            value = value << column
            total += value
            column += 1
        return total

    def z_gates_value(self):
        total = 0
        column = 0
        while True:
            if not self.has_value("z" + format(column, '02')):
                break
            value = 1 if self.value("z" + format(column, '02')) else 0
            value = value << column
            total += value
            column += 1
        return total
    
    def set_input(self, operand, value):
        for n in range(45):
            self.set_wire_value(operand + format(n, '02'), bool((value >> n) & 1))

            
with open("input_fixed.txt") as f:
    lines = f.readlines()


for n in range(1, 45):
    circuit = Circuit()
    for line in lines:
        if "->" in line:
            left, operator, right, _, destination = line.strip().split(" ")
            circuit.add_gate(destination, left, operator, right)

    circuit.set_input("x", 0)
    circuit.set_input("y", 0)
    circuit.set_wire_value("x" + format(n, '02'), True)
    circuit.set_wire_value("y" + format(n, '02'), True)
    circuit.evaluate_fully()
    if circuit.wires_value("x") + circuit.wires_value("y")  == circuit.z_gates_value():
        print("Passed with", format(n, '02'))
    else:
        print("--------")
        print("Failed with", format(n, '02'))
        print("Binary representations:")
        print("{:045b}".format(circuit.wires_value("x")))
        print("{:045b}".format(circuit.wires_value("y")))
        print("=")
        print("{:045b}".format(circuit.z_gates_value()))
        break
