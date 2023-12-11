from aocd import data
import re

class Grid:
    grid: [str]
    loop_only: [str]
    start_loc: tuple

    def __init__(self, data, part=1):
        self.setup_dirs()
        self.grid = data.splitlines()
        self.start_loc = (0,0)
        self.loop_only = []
        for y,line in enumerate(self.grid):
            self.loop_only.append('.' * len(line))
            s = line.find('S')
            if s > -1:
                self.start_loc = (s,y)

    def run(self, part=1):
        # find start direction
        (x,y) = self.start_loc
        start_dir = None
        if x > 0 and self.pipe(( x-1, y) ) in '-FL':
            start_dir = (-1,0)
        elif y > 0 and self.pipe( (x,y-1) ) in '|F7':
            start_dir = (0,-1)
        elif y < len(self.grid)-1 and self.pipe( (x,y+1) ) in '|JL':
            start_dir = (0,1)
        
        steps = 0
        loc = self.start_loc
        cur_dir = start_dir
        following = True
        # follow path around
        while following:
            loc = (loc[0] + cur_dir[0], loc[1] + cur_dir[1])
            steps += 1
            pipe = self.pipe(loc)
            if pipe == 'S':
                following = False
                # for loop-only, figure out what kind of transition point the S location is.
                for ch in self.dirs.keys():
                    if cur_dir in self.dirs[ch] and self.dirs[ch][cur_dir] == start_dir:
                        pipe = ch
            else:
                cur_dir = self.dirs[pipe][cur_dir]
    
            self.loop_only[loc[1]] = self.loop_only[loc[1]][:loc[0]] + pipe + self.loop_only[loc[1]][loc[0] + 1:]
        if part == 1:
            return (steps+1) // 2
        
        # use loop_only section to count interior tiles. Every . is either inside or outside
        inside_cnt = 0
        for y, line in enumerate(self.loop_only):
            idx = -1
            while True:
                idx = line.find('.', idx + 1)
                if idx > -1:
                    inside_cnt += 1 if self.inside( (idx, y) ) else 0
                else:
                    break

        return inside_cnt
    
    def inside(self, loc):
        if loc[0] < 0 or loc[1] < 0:
            return False
        if self.loop(loc) in '.L7':
            return self.inside( (loc[0] - 1, loc[1] - 1) )
        return not self.inside( (loc[0] - 1, loc[1] - 1) )

    def setup_dirs(self):
        dirstrlist = '''-:1,0->1,0
|:0,1->0,1
7:1,0->0,1
J:1,0->0,-1
F:-1,0->0,1
L:-1,0->0,-1
'''
        self.dirs = {}
        for dirstr in dirstrlist.splitlines():
            match = re.match('^(.):(.*),(.*)->(.*),(.*)$', dirstr)
            ch,sx,sy,dx,dy = match.groups()
            m = {}
            m[( int(sx),int(sy) )] = ( int(dx), int(dy) )
            m[( -int(dx), -int(dy) )] = ( -int(sx), -int(sy) )
            self.dirs[ch] = m
        

    def pipe(self, loc):
        return self.grid[loc[1]][loc[0]]
    def loop(self, loc):
        return self.loop_only[loc[1]][loc[0]]


def run(data, part=1):
    return Grid(data, part).run(part)

ex1='''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
'''
ex2='''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
'''

assert run(ex1) == 8
print('10a: ', run(data))
assert run(ex2, part=2) == 10
print('10b: ', run(data, part=2))