from aocd import data

class CrabCups:
    def __init__(self):
        self.cups = []

    @classmethod
    def from_cups_str(cls, cups_str, max_num = -1):
        cups = cls()
        cups.cups = [int(x) for x in cups_str]
        if max_num > len(cups.cups):
            for x in range(max(cups.cups), max_num):
                cups.cups.append(x)
        return cups

    def move(self):
        # note current cup
        cur_cup = self.cups[0]
        # yank next three
        collected_cups = self.cups[1:4]
        self.cups = self.cups[:1] + self.cups[4:]
        # get dest cup
        destination_cup = cur_cup - 1
        while destination_cup in collected_cups or destination_cup < min(self.cups):
            destination_cup -= 1
            if destination_cup < min(self.cups):
                destination_cup = max(self.cups)
        dest_idx = self.cups.index(destination_cup)
        # put collected cups back
        self.cups = self.cups[:dest_idx + 1] + collected_cups + self.cups[dest_idx + 1:]
        # rotate array so that next cup is at start
        self.cups = self.cups[1:] + self.cups[:1]

    def play(self, num_moves):
        for move in range(num_moves):
            self.move()
        # rotate to cup 1
        idx = self.cups.index(1)
        self.cups = self.cups[idx:] + self.cups[:idx]
        result = ''.join([str(x) for x in self.cups[1:]])
        return result

    def play2(self, num_moves):
        for move in range(num_moves):
            if move % 100000 == 0: print('.', end='')
            self.move()
        # rotate to cup 1
        idx = self.cups.index(1)
        self.cups = self.cups[idx:] + self.cups[:idx]
        result = self.cups[1] * self.cups[2]
        return result


assert CrabCups.from_cups_str('389125467').play(10) == '92658374'
assert CrabCups.from_cups_str('389125467').play(100) == '67384529'
print('23a: ', CrabCups.from_cups_str('364297581').play(100))

assert CrabCups.from_cups_str('389125467', 1000000).play2(10000000) == 149245887792
print('23b: ', CrabCups.from_cups_str('364297581', 1000000).play2(10000000))

