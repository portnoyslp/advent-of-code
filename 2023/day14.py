from aocd import data

class Dish:
    north = (0,-1)
    south = (0,1)
    west = (-1,0)
    east = (1,0)

    def __init__(self, data):
        self.rows = data.splitlines()
        self.boulder_locations = set()
        self.rock_locations = set()
        for yp, row in enumerate(self.rows):
            for xp, ch in enumerate(row):
                if ch == 'O':
                    self.boulder_locations.add( (xp, yp) )
                elif ch == '#':
                    self.rock_locations.add( (xp, yp) )

    def run_cycle(self):
        self.roll(self.north)
        self.roll(self.west)
        self.roll(self.south)
        self.roll(self.east)

    def cycle(self, count):
        # store last limit locations
        boulder_location_hash={}
        for i in range(count):
            self.run_cycle()
            fset = frozenset(self.boulder_locations)
            if fset in boulder_location_hash:
                # we've reached a steady state, so just short circuit loop.
                loop_length = i - boulder_location_hash[fset] - 1
                print(f'After {i+1} cycles, found a {loop_length}-cycle loop')
                # should do last n cycles to finish loop for remaining count?
                modulus = (count - i + 2) % loop_length
                for k in range(modulus):
                    self.run_cycle()
                return self
            boulder_location_hash[fset] = i
        return self

    def roll_and_get_load(self) -> int:
        self.roll(self.north)
        #print(self)
        return self.calc_load()
    
    def roll(self, dir):
        # move all boulders in the given direction until they stop.
        if dir in [self.north, self.south]:
            key = lambda x: x[1]
        else:
            key = lambda x: x[0]
        reverse = dir in [self.south,self.east]
        boulders = sorted(self.boulder_locations, key=key, reverse=reverse)
        for boulder in boulders:
            while True:
                new_pos = (boulder[0] + dir[0], boulder[1] + dir[1])
                if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= len(self.rows[0]) or new_pos[1] >= len(self.rows):
                    # boulder can't move off screen
                    break
                if new_pos in self.boulder_locations or new_pos in self.rock_locations:
                    # There's something in the way
                    break
                # boulder can move
                self.boulder_locations.remove(boulder)
                self.boulder_locations.add(new_pos)
                boulder = new_pos

    def calc_load(self) -> int:
        return sum([len(self.rows) - x[1] for x in self.boulder_locations])

    def __str__(self) -> str:
        str = ''
        for yp in range(len(self.rows)):
            str += ('\n' if yp > 0 else '')
            for xp in range(len(self.rows[0])):
                t = (xp,yp)
                str += ('O' if t in self.boulder_locations else '#' if t in self.rock_locations else '.')
        return str
    
    def __repr__(self) -> str:
        return 'Dish<load=' + self.calc_load() + '>'
    

def run(data, part=1):
    if part == 2:
        return Dish(data).cycle(1000000000).calc_load()
    return Dish(data).roll_and_get_load()

ex1='''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''

assert run(ex1) == 136
print('14a: ', run(data))
assert run(ex1, part=2) == 64
print('14b: ', run(data, part=2))