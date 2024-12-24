class Circuit():
    def __init__(self):
        self.wires = {}
        self.gates = {}
        self.evaluated_gates = {}

    def set_wire_value(self, wire, value):
        self.wires[wire] = bool(value)

    def add_gate(self, wire, left, operator, right):
        self.gates[wire] = (left, operator, right)

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
            
with open("input.txt") as f:
    lines = f.readlines()

circuit = Circuit()

for line in lines:
    if ": " in line:
        wire, value = line.strip().split(": ")
        circuit.set_wire_value(wire, True if value == "1" else False)
    elif "->" in line:
        left, operator, right, _, destination = line.strip().split(" ")
        circuit.add_gate(destination, left, operator, right)

circuit.evaluate_fully()
print(circuit.z_gates_value())