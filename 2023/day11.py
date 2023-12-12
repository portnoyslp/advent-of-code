from aocd import data
import re

def run(data, expansion=2):
    lines = data.splitlines()
    (lines_to_expand, cols_to_expand) = expansions(lines)
    coords = star_coords(lines)
    dist_sum = 0
    for idx, c1 in enumerate(coords):
        for c2 in coords[idx+1:]:
            dist = abs(c1[0]-c2[0]) + abs(c1[1] - c2[1])
            # count expansions between coords.
            for xp in cols_to_expand:
                if (c1[0] < xp < c2[0]) or (c2[0] < xp < c1[0]):
                    dist += (expansion - 1)
            for yp in lines_to_expand:
                if (c1[1] < yp < c2[1]) or (c2[1] < yp < c1[1]):
                    dist += (expansion - 1)
            dist_sum += dist
    return dist_sum

def star_coords(lines):
    coords = []
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == '#':
                coords.append( (x,y) )
    return coords

def expansions(lines):
    lines_to_expand = []
    cols_to_expand = list(range(len(lines[0])))
    for idx,line in enumerate(lines):
        if re.match('^\.+$', line):
            lines_to_expand.append(idx)
        else:
            i = 0
            while i != -1:
                i = line.find('#', i)
                if i > -1:
                    if i in cols_to_expand:
                        cols_to_expand.remove(i)
                    i += 1
    return (lines_to_expand, cols_to_expand)

ex1='''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''

assert run(ex1) == 374
print('11a: ', run(data))
assert run(ex1, expansion=10) == 1030
assert run(ex1, expansion=100) == 8410
print('11b: ', run(data, expansion=1000000))