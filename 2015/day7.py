from aocd import data
import re


class LogicGates:
    def __init__(self):
        self.wires = {}
        self.inputs = {}
        self.dispatch = {'NOT': self._not, 'AND': self._and, 'OR': self._or, 'LSHIFT': self.lshift,
                         'RSHIFT': self.rshift, 'ASSIGN': self.assign}

    def connect(self, line):
        match = re.match(r'(\d+|\w+) -> (\w+)', line)
        if match:
            self.inputs[match.group(2)] = ('ASSIGN', match.group(1))
        match = re.match(r'NOT (\w+) -> (\w+)', line)
        if match:
            self.inputs[match.group(2)] = ('NOT', match.group(1))
        match = re.match(r'(\d+|\w+) (AND|OR|LSHIFT|RSHIFT) (\d+|\w+) -> (\w+)', line)
        if match:
            self.inputs[match.group(4)] = (match.group(2), match.group(1), match.group(3))

    def resolvable(self, wire):
        if wire in self.wires:
            return True
        input = self.inputs[wire]
        return all([(val[0].isalpha() and val in self.wires) or val[0].isdigit() for val in input[1:]])

    def resolve_any(self):
        unresolved_keys = set(self.inputs.keys()) - set(self.wires.keys())
        for wire in [w for w in unresolved_keys if self.resolvable(w)]:
            self.resolve(wire)

    def resolve(self, wire):
        input = self.inputs[wire]
        if type(input) is int:
            self.wires[wire] = input
            return
        op = input[0]
        self.wires[wire] = self.dispatch[op](*input[1:])

    def assign(self, val):
        return self.ref(val)

    def _not(self, val):
        return ~self.ref(val) & 0xffff

    def _and(self, val1, val2):
        return self.ref(val1) & self.ref(val2)

    def _or(self, val1, val2):
        return self.ref(val1) | self.ref(val2)

    def lshift(self, val1, val2):
        return self.ref(val1) << self.ref(val2)

    def rshift(self, val1, val2):
        return self.ref(val1) >> self.ref(val2)

    def ref(self, val):
        value = int(val) if val[0].isdigit() else self.wires[val]
        return value

    def connections(self, input_str, resolve=True):
        for line in input_str.splitlines():
            self.connect(line)
        if resolve:
            self.run_resolve()
        return self

    def run_resolve(self):
        while set(self.inputs.keys()) != set(self.wires.keys()):
            self.resolve_any()
        return self



assert LogicGates().connections('''123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i''').wires == {'d': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412, 'i': 65079, 'x': 123, 'y': 456}
print('7a: ', LogicGates().connections(data).wires['a'])

override_value = LogicGates().connections(data).wires['a']
gates = LogicGates().connections(data, resolve=False)
gates.connect(f"{override_value} -> b")
print('7b: ', gates.run_resolve().wires['a'])
