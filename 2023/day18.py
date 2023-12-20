from aocd import data
import re

dirs = {'R': (1,0), 'L': (-1,0), 'D': (0,1), 'U': (0,-1)}

def run(data, part=1):
    loc = (0,0)
    coords = [loc]
    shoelace = 0
    perimeter = 0
    for line in data.splitlines():
        dir, dist = dir_and_dist(line, part)
        nextloc = new_loc(loc, dir, dist)
        perimeter += dist
        coords.append(nextloc)
        det = nextloc[1] * loc[0] - nextloc[0] * loc[1]
        shoelace += det
        loc = nextloc
    double_area = shoelace + perimeter
    return double_area // 2 + 1

def new_loc(loc, dir, dist):
    return ( loc[0] + dist*dirs[dir][0], loc[1] + dist*dirs[dir][1])

def dir_and_dist(line, part):
    dir, dist, color = re.match('(.) (\d+) \((\#[0-9a-f]+)\)', line).groups()
    if part == 1:
        return dir, int(dist)
    dist = int(color[1:6], 16)
    dir = 'RDLU'[int(color[6])]
    return dir,dist

ex1='''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''

assert run(ex1) == 62
print('18a: ', run(data))
assert run(ex1, part=2) == 952408144115
print('18b: ', run(data, part=2))