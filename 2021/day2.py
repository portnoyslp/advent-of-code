import posixpath
from aocd import lines

def run_directions(lines, use_aim = False):
    depth = 0
    pos = 0
    aim = 0
    for line in lines:
        dir, dist = line.split()
        dist = int(dist)
        if (dir == 'forward'):
            pos += dist
            if use_aim:
                depth += aim * dist        
        elif (dir == 'up'):
            if use_aim:
                aim -= dist
            else:
                depth -= dist
        else:
            if use_aim:
                aim += dist
            else:
                depth += dist
    return depth * pos


ex1 = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
assert run_directions(ex1.splitlines()) == 150
print('2a: ', run_directions(lines))

assert run_directions(ex1.splitlines(), True) == 900
print('2b: ', run_directions(lines, True))
