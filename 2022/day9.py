from aocd import data

dirs = {'R': [1,0], 'L': [-1,0], 'U': [0,-1], 'D': [0,1]}

def num_pos_visited(data):
    directions = data.splitlines()
    head_pos = [0,0]
    tail_pos = [0,0]
    visited = {tuple(tail_pos)}
    for direction in directions:
        vec = dirs[direction[0]]
        dist = int(direction[2:])
        for i in range(dist):
            head_pos = [sum(x) for x in zip(head_pos,vec)]
            tail_pos = _adjust_tail(head_pos,tail_pos)
            visited.add(tuple(tail_pos))
    return len(visited)

def _adjust_tail(head_pos, tail_pos):
    if abs(tail_pos[0] - head_pos[0]) > 1 and abs(tail_pos[1] - head_pos[1]) > 1:
        return [int((tail_pos[0] + head_pos[0])/ 2), int((tail_pos[1] + head_pos[1])/ 2)]
    if abs(tail_pos[0] - head_pos[0]) > 1:
        return [int((tail_pos[0] + head_pos[0])/ 2), head_pos[1]]
    if abs(tail_pos[1] - head_pos[1]) > 1:
        return [head_pos[0], int((tail_pos[1] + head_pos[1])/ 2)]
    return tail_pos

def long_rope_visits(data, printing=False):
    directions = data.splitlines()
    rope_len = 10
    rope = [ tuple([0,0]) for x in range(rope_len)]
    visited = {(rope[rope_len - 1])}
    for direction in directions:
        vec = dirs[direction[0]]
        dist = int(direction[2:])
        for i in range(dist):
            rope[0] = [sum(x) for x in zip(rope[0],vec)]
            for i in range(1,rope_len):
                rope[i] = tuple(_adjust_tail(rope[i - 1], rope[i]))
            visited.add(rope[rope_len - 1])
            if printing:
                _printout(rope, range(0,6), range(-4,1))
        if printing:
            print('== ' + direction + ' ==')
            _printout(rope, range(0,6), range(-4,1))
    return len(visited)

def _printout(rope, xrange, yrange):
    for y in yrange:
        for x in xrange:
            output = False
            for idx,coord in enumerate(rope):
                if coord[0] == x and coord[1] == y:
                    if idx == 0:
                        print('H',end='')
                    else:
                        print(idx,end='')
                    output = True
                    break
            if not(output):       
                if x == 0 and y == 0:
                    print('s',end='')
                else:
                    print('.', end='')
        print('')
    print ('')
    
                

ex1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

assert num_pos_visited(ex1) == 13
print ('9a: ', num_pos_visited(data))

ex2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
assert long_rope_visits(ex1, True) == 1
assert long_rope_visits(ex2) == 36
print ('9b: ', long_rope_visits(data))
