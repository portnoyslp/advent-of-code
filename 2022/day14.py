from aocd import data


class Cave:
    def __init__(self,data, part=1):
        self.start=(500,0)
        self.walls=set()
        self.filled=set()
        self.part = part
        self.build_walls(data)
 
    def build_walls(self, data):
        for line in data.splitlines():
            starting = True
            start_coord = None
            for coord in line.split(' -> '):
                if not starting:
                    axes = self.make_tuple(coord)
                    (sx,sy) = start_coord
                    if sx == axes[0]:
                        for y in range(min(sy,axes[1]), max(sy,axes[1]) + 1):
                            self.walls.add((sx,y))
                    else:
                        for x in range(min(sx,axes[0]), max(sx,axes[0]) + 1):
                            self.walls.add((x,sy))
                starting = False
                start_coord = self.make_tuple(coord)
        self.limit = max([t[1] for t in self.walls]) + 2
        self.filled = set(self.walls)
    
    def make_tuple(self,coord):
        return tuple([int(x) for x in coord.split(',')])
    
    def occupied(self, coord):
        if coord[1] == self.limit and self.part==2:
            return True
        return coord in self.filled
    
    def count_sand_units(self):
        cnt = 0
        while True:
            if self.occupied(self.start): # part 2
                return cnt
            sand = self.process_sand()
            if sand == None:
                return cnt
            cnt += 1
            self.filled.add(sand)
        
    def process_sand(self):
        sand = self.start
        while True:
            new_sand = self.update_sand(sand)
            if new_sand == None:
                # stopped moving
                return sand;
            sand = new_sand
            if sand[1] >= self.limit:
                # reached limit, signal that we're done
                return None

    def update_sand(self, sand):
        (sx,sy) = sand
        if self.occupied((sx,sy+1)):
            if self.occupied((sx-1,sy+1)):
                if self.occupied((sx+1,sy+1)):
                    return None
                return (sx+1,sy+1)
            return (sx-1,sy+1)
        return (sx,sy+1)


ex1='''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
assert(Cave(ex1).count_sand_units() == 24)
print('14a: ', Cave(data).count_sand_units())
assert(Cave(ex1, part=2).count_sand_units() == 93)
print('14b: ', Cave(data, part=2).count_sand_units())