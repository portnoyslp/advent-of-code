from aocd import data


class Houses:
    DIRS = {'^': (0, -1), '>': (1, 0), '<': (-1, 0), 'v': (0, 1)}

    def __init__(self, num_santas=1):
        self.locs = [(0, 0)] * num_santas
        self.visited = set()
        self.santa_idx = 0

    def move(self, char):
        self.locs[self.santa_idx] = tuple(map(sum, zip(self.locs[self.santa_idx], self.DIRS[char])))
        self.santa_idx = (self.santa_idx + 1) % len(self.locs)

    def moves(self, input_str):
        self.visited.update(self.locs)
        for c in input_str:
            self.move(c)
            self.visited.update(self.locs)
        return len(self.visited)


assert Houses().moves('>') == 2
assert Houses().moves('^>v<') == 4
assert Houses().moves('^v^v^v^v^v') == 2
print('3a: ', Houses().moves(data))

assert Houses(2).moves('>v') == 3
assert Houses(2).moves('^>v<') == 3
assert Houses(2).moves('^v^v^v^v^v') == 11
print('3b: ', Houses(2).moves(data))
