import cProfile

class CrabCups:
    def __init__(self):
        self.cups = []

    @classmethod
    def from_cups_str(cls, cups_str, max_num=-1):
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


assert CrabCups.from_cups_str('389125467').play(10) == '92658374'
assert CrabCups.from_cups_str('389125467').play(100) == '67384529'
print('23a: ', CrabCups.from_cups_str('364297581').play(100))


class CrabCups2:
    def __init__(self):
        # Use a special linked list form, in which we have an array of indexes to the next
        # item. Array will start with 1, basically.
        self.start = -1
        self.ptr_array = []
        self.max_cup = -1

    @classmethod
    def from_cups_str(cls, cups_str, max_num=-1):
        cups = cls()
        cup_values = [int(c) for c in cups_str]
        max_value = max_num if max_num > -1 else max(cup_values)
        cups.ptr_array = [0] * (max_value+1)

        first_new_cup = max(cup_values) + 1
        for idx, cup in enumerate(cup_values):
            if idx < len(cup_values) - 1:
                cups.ptr_array[cup] = cup_values[idx + 1]
            else:
                # We're at the end, and now we pad
                cups.ptr_array[cup] = cup_values[0] if max_num == -1 else first_new_cup
        for val in range(first_new_cup, max_num):
            cups.ptr_array[val] = val + 1
        if max_num != -1:
            cups.ptr_array[max_num] = cup_values[0]
        cups.start = cup_values[0]
        cups.max_cup = max_num if max_num > -1 else max(cup_values)
        return cups

    def print_cups(self):
        c = []
        cup = self.start
        for _ in range(len(self.ptr_array)):
            c.append(cup)
            cup = self.ptr_array[cup]
        print(' '.join(map(str, c)))

    def move(self):
        # yank next three
        collected_cups = []
        c = self.start
        for _ in range(3):
            collected_cups.append(self.ptr_array[c])
            c = self.ptr_array[c]
        # get dest cup
        destination_cup = self.start - 1
        while destination_cup in collected_cups or destination_cup < 1:
            destination_cup -= 1
            if destination_cup < 1:
                destination_cup = self.max_cup
        # move the three collected cups to after the destination cup. This involves:
        # 1. pointing the cur_cup to the one after the collected group.
        # 2. pointing the tail of the collected group to the one after destination cup.
        # 3. pointing the destination cup to the start of the group.
        self.ptr_array[self.start] = self.ptr_array[collected_cups[-1]]
        self.ptr_array[collected_cups[-1]] = self.ptr_array[destination_cup]
        self.ptr_array[destination_cup] = collected_cups[0]
        # set next cup to start
        self.start = self.ptr_array[self.start]

    def play(self, num_moves):
        for move in range(num_moves):
            self.move()
            #self.print_cups()
        val1 = self.ptr_array[1]
        val2 = self.ptr_array[val1]
        return val1 * val2



assert CrabCups2.from_cups_str('389125467', 1000000).play(10000000) == 149245887792
print('23b: ', CrabCups2.from_cups_str('364297581', 1000000).play(10000000))
