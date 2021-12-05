from aocd import lines
import re
from collections import defaultdict

def count_intersections(inputlines, include_diagonals = False):
    lines = parse_lines(inputlines)
    coords = generate_line_coords(lines, include_diagonals)
    return count_crossing_coords(coords)

def parse_lines(inputlines):
    lines = []
    for line in inputlines:
        (x1,y1,x2,y2) = map(int, re.match("(\d+),(\d+) -> (\d+),(\d+)", line).groups())
        lines.append( ((x1, y1), (x2, y2)) )
    return lines

def cmp(a, b):
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def generate_line_coords(lines, include_diagonals = False):
    coords = defaultdict(int)
    for (c1, c2) in lines:
        dx = c2[0] - c1[0]
        dy = c2[1] - c1[1]
        if dx == 0:
            for y in range(c1[1], c2[1], -1 if c1[1] > c2[1] else 1):
                coords[(c1[0], y)] += 1
            coords[c2] += 1
        elif dy == 0:
            for x in range(c1[0], c2[0], -1 if c1[0] > c2[0] else 1):
                    coords[(x, c1[1])] += 1
            coords[c2] += 1  
        elif include_diagonals and abs(dx) == abs(dy):
            for diff in range(0, abs(dx)):
                coords[ (c1[0] + diff * cmp(c2[0], c1[0]), c1[1] + diff * cmp(c2[1], c1[1])) ] += 1
            coords[c2] += 1
    return coords

def count_crossing_coords(coords):
    crossings = [x for x in coords.values() if x > 1]
    return len(crossings)

test = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

assert count_intersections(test.splitlines()) == 5
print('5a: ', count_intersections(lines))

assert count_intersections(test.splitlines(), True) == 12
print('5b: ', count_intersections(lines, True))
