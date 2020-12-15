
class MemoryGame:
    def __init__(self, start_list):
        self.last_spoken_idx = 0
        self.start_list = start_list
        self.last_spoken = None
        self.last_seen = {}

    def get_next(self):
        if self.last_spoken_idx < len(self.start_list):
            ret = self.start_list[self.last_spoken_idx]
        else:
            if self.last_spoken in self.last_seen:
                ret = self.last_spoken_idx - self.last_seen[self.last_spoken]
            else:
                ret = 0
        self.last_seen[self.last_spoken] = self.last_spoken_idx
        self.last_spoken_idx += 1
        self.last_spoken = ret
        return self.last_spoken

    def get_nth(self, idx):
        while self.last_spoken_idx < idx:
            last = self.get_next()
        return last


def part1(start_list):
    return MemoryGame(start_list).get_nth(2020)
def part2(start_list):
    return MemoryGame(start_list).get_nth(30000000)

assert part1([0,3,6]) == 436
assert part1([1,3,2]) == 1
assert part1([2,1,3]) == 10
assert part1([1,2,3]) == 27
assert part1([2,3,1]) == 78
assert part1([3,2,1]) == 438
assert part1([3,1,2]) == 1836
print ('15a: ', part1([12,20,0,6,1,17,7]))

assert part2([0,3,6]) == 175594
assert part2([1,3,2]) == 2578
assert part2([2,1,3]) == 3544142
assert part2([1,2,3]) == 261214
assert part2([2,3,1]) == 6895259
assert part2([3,2,1]) == 18
assert part2([3,1,2]) == 362
print ('15b: ', part2([12,20,0,6,1,17,7]))
