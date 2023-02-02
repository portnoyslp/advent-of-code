from aocd import data

def step(array):
    copy = [x[:] for x in array]
    moves = 0
    for y, line in enumerate(array):
        for x, ch in enumerate(line):
            if ch == '>':
                target = (x+1) % len(line)
                if array[y][target] == '.':
                    moves += 1
                    copy[y][target] = '>'
                    copy[y][x] = '.'
    array = copy
    copy = [x[:] for x in array]
    for y, line in enumerate(array):
        for x, ch in enumerate(line):
            if ch == 'v':
                target = (y+1) % len(array)
                if array[target][x] == '.':
                    moves += 1
                    copy[target][x] = 'v'
                    copy[y][x] = '.'
    return (copy, moves)

def aprint(array):
    for l in array:
        print("".join(l))
    print("")

def count_until_frozen(inputdata):
    array = []
    for line in inputdata.splitlines():
        array.append(list([x for x in line]))
    num_steps = 0
    # aprint(array)
    while True:
        num_steps += 1
        (array, moves) = step(array)
        # aprint(array)
        if moves == 0:
            break
    return num_steps

test = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""
assert(count_until_frozen(test) == 58)
print('25a: ', count_until_frozen(data))
