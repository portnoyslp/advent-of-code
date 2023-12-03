from aocd import data
import re
from collections import defaultdict
from math import prod

def count_parts(data):
    lines = data.splitlines()
    sum = 0
    for rownum, line in enumerate(lines):
        for match in re.finditer('\d+', line):
            if symbol_in_rect(lines, match.start() - 1, rownum - 1, match.end(), rownum +1):
                sum += int(match.group())
    return sum

def symbol_in_rect(lines, sx, sy, ex, ey, only_gear=False):
    for x in range(max(0,sx), min(ex + 1,len(lines[0]))):
        for y in range(max(0,sy), min(ey + 1,len(lines))):
            if only_gear and lines[y][x] == '*':
                return (x,y)
            if lines[y][x] != '.' and not lines[y][x].isnumeric():
                return (x,y)
    return None

def count_gears(data):
    lines = data.splitlines()
    gears = defaultdict(list)
    for rownum, line in enumerate(lines):
        for match in re.finditer('\d+', line):
            gearpos = symbol_in_rect(lines, match.start() - 1, rownum - 1, match.end(), rownum +1, only_gear=True)
            if gearpos:
                gears[gearpos].append(int(match.group()))
    return sum([prod(x) for x in gears.values() if len(x) == 2])

ex1='''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''

assert(count_parts(ex1) == 4361)
print('3a: ', count_parts(data))
assert(count_gears(ex1) == 467835)
print('3b: ', count_gears(data))
