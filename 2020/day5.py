from aocd import data
import re

def seat_id(spec):
    # regex replace to binary digits, and then parse as integer
    spec = re.sub('F', '0', spec)
    spec = re.sub('B', '1', spec)
    spec = re.sub('R', '1', spec)
    spec = re.sub('L', '0', spec)
    return int(spec, 2)

def max_seat_id(input):
    return max([seat_id(spec) for spec in input.split()])

def find_gap(input):
    seats = sorted([seat_id(spec) for spec in input.split()])
    for idx in seats[1:]:
        if seats[idx] - seats[idx-1] > 1:
            return seats[idx] - 1

assert seat_id('BFFFBBFRRR') == 567
assert seat_id('FFFBBBFRRR') == 119
assert seat_id('BBFFBBFRLL') == 820

print(f'5a: {max_seat_id(data)}')
print(f'5b: {find_gap(data)}')