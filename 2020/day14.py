from aocd import data
import re
import itertools

class Docking:
    def __init__(self):
        self.memory = {}
        self.and_mask = -1
        self.or_mask = 0

    def set_mask(self, mask_str):
        self.and_mask = int(mask_str.replace('X', '1'), 2)
        self.or_mask = int(mask_str.replace('X', '0'), 2)

    def set_memory(self, loc, val):
        val &= self.and_mask
        val |= self.or_mask
        self.memory[loc] = val

    def dispatch(self, line):
        if line == '':
            return
        var, val = re.match(r'([a-z\[\]0-9]+) = (\w+)$', line).groups()
        if var == 'mask':
            self.set_mask(val)
        else:
            loc = re.match(r'\w+\[(\d+)\]', var).group(1)
            self.set_memory(int(loc), int(val))

    def run(self, input_str):
        for line in input_str.splitlines():
            self.dispatch(line)
        return sum(self.memory.values())

assert Docking().run('''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0''') == 165
print('14a: ', Docking().run(data))

class Docking2(Docking):
    def __init__(self):
        Docking.__init__(self)
        self.cur_mask = '0'

    def set_mask(self, mask_str):
        self.cur_mask = mask_str

    def update_float_locs(self, loc_str, combo):
        for c in combo:
            loc_str = loc_str.replace('X', c, 1)
        return loc_str

    def set_memory(self, loc, val):
        mask_len = len(self.cur_mask)
        loc_str = f'{{0:0{mask_len}b}}'.format(loc)
        for idx, bitval in enumerate(self.cur_mask):
            if bitval != '0':
                loc_str = loc_str[0:idx] + bitval + loc_str[idx+1:]
        num_floats = loc_str.count('X')
        locs = []
        for combo in itertools.product('01', repeat=num_floats):
            locs.append(int(self.update_float_locs(loc_str, combo), 2))
        for loc in locs:
            self.memory[loc] = val

assert Docking2().run('''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1''') == 208
print('14b: ', Docking2().run(data))
