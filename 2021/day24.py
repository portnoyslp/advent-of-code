from aocd import lines
import itertools



class ALU:
    def __init__(self, instructions):
        self.instructions = instructions
        self.iptr = 0
        self.vars = {'x':0,'y':0,'z':0,'w':0}
        self.inputs = []      
        self.ops = {
            'inp': self.__inp,'add': self.__add,'mul': self.__mul,
            'div': self.__div,'mod': self.__mod,'eql': self.__eql
        }

    def __inp(self, args):
        loc = args[0]
        self.vars[loc] = self.inputs.pop()
    
    def __add(self, args):
        (loc, operand) = args
        self.vars[loc] += self.vars[operand] if operand in self.vars else int(operand)

    def __mul(self, args):
        (loc, operand) = args
        self.vars[loc] *= self.vars[operand] if operand in self.vars else int(operand)

    def __div(self, args):
        (loc, operand) = args
        self.vars[loc] //= self.vars[operand] if operand in self.vars else int(operand)

    def __mod(self, args):
        (loc, operand) = args
        self.vars[loc] %= self.vars[operand] if operand in self.vars else int(operand)

    def __eql(self, args):
        (loc, operand) = args
        val = self.vars[operand] if operand in self.vars else int(operand)
        self.vars[loc] = 1 if val == self.vars[loc] else 0
    
    def run(self):
        self.iptr = 0
        self.vars = {'x':0,'y':0,'z':0,'w':0}
        while self.iptr < len(self.instructions):
            tokens = self.instructions[self.iptr].split(' ')
            f = self.ops[tokens[0]](tokens[1:])
            self.iptr += 1

    def input(self, input_vals):
        for val in input_vals:
            self.inputs.insert(0, val)

    def validate_model_id(self, id):
        self.input(map(int, [x for x in id]))
        self.run()
        return self.vars['z'] == 0

engine = ALU(lines)
for id in itertools.product('987654321', repeat=14):
    if engine.validate_model_id(id):
        print('24a: ', id)
        break            