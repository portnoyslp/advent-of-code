from aocd import data


def find_floor(input_str):
    up = input_str.count('(')
    down = input_str.count(')')
    return up - down


assert find_floor('(())') == find_floor('()()') == 0
assert find_floor('(((') == find_floor('(()(()(') == find_floor('))(((((') == 3
assert find_floor('())') == find_floor('))(') == -1
assert find_floor(')))') == find_floor(')())())') == -3
print('1a: ', find_floor(data))


def basement_index(input_str):
    floor = 0
    for i, val in enumerate(input_str):
        if val == '(':
            floor += 1
        elif val == ')':
            floor -= 1
        if floor == -1:
            return i + 1


assert basement_index(')') == 1
assert basement_index('()())') == 5
print('1b: ', basement_index(data))
