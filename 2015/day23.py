from aocd import data
import re

class Machine:
    def __init__(self, input_str):
        self.instructions = []
        for line in input_str.splitlines():
            (op, reg_or_offset, _, offset_str) = re.match(r'(.{3}) ([^,]+)(, ([0-9+-]+))?', line).groups()
            reg = ''
            offset = 0
            if reg_or_offset in ('a', 'b'):
                reg = reg_or_offset
                if offset_str:
                    offset = int(offset_str)
            else:
                offset = int(reg_or_offset)
            self.instructions.append((op, reg, offset))
        self.ip = 0
        self.registers = {'a': 0, 'b': 0}
        self.op_dict = {'hlf': self.halve, 'tpl': self.triple, 'inc': self.increment, 'jmp': self.jump, 'jie': self.jump_if_even, 'jio': self.jump_if_one}

    def halve(self, op, reg, _):
        self.registers[reg] /= 2
        self.ip += 1

    def triple(self, op, reg, _):
        self.registers[reg] *= 3
        self.ip += 1

    def increment(self, op, reg, _):
        self.registers[reg] += 1
        self.ip += 1

    def jump(self, op, _, offset):
        self.ip += offset

    def jump_if_even(self, op, reg, offset):
        if self.registers[reg] % 2 == 0:
            self.jump(op, '', offset)
        else:
            self.ip += 1

    def jump_if_one(self, _, reg, offset):
        if self.registers[reg] == 1:
            self.jump('', '', offset)
        else:
            self.ip += 1

    def run(self):
        while self.ip < len(self.instructions):
            inst = self.instructions[self.ip]
            self.op_dict[inst[0]](*inst)
        return self.registers['b']

print('23a: ', Machine(data).run())
part2 = Machine(data)
part2.registers['a'] = 1
print('23b: ', part2.run())


