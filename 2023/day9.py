from aocd import data
from functools import reduce
from operator import add,sub

def diffs(l, p2=False):
    if all(x == 0 for x in l):
        return 0

    N = []
    for x in range(1, len(l)):
        N.append(l[x] - l[x-1])

    op = add
    pos = -1
    if p2:
        op = sub
        pos = 0
    return op(l[pos], diffs(N, p2))

def run(data, part=1):
    lines = data.splitlines()
    total = 0
    for line in lines:
        cur_row = [int(x) for x in line.split()]
        cur_sum = extrapolate(cur_row, part)
        if cur_sum != diffs(cur_row, part==2):
            print ('Mismatch for ', cur_row, '(',cur_sum,' vs ',diffs(cur_row,part==2),')')
        total += cur_sum
    return total

def extrapolate(init_row, part=1):
    rows = []
    cur_row = init_row
    rows.append(cur_row)
    reducing = True
    while reducing:
        zipped_vals = zip(cur_row[:-1],cur_row[1:])
        new_row = [y-x for x,y in zipped_vals]
        rows.append(new_row)
        if all(x == 0 for x in new_row):
            reducing = False
        cur_row = new_row
    if part==1:
        last_elts = [row[-1] for row in rows]
        return sum(last_elts)
    first_elts = [row[0] for row in rows]
    reduction = reduce(lambda x,y:y-x, reversed(first_elts))
    return reduction

ex1='''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

assert run(ex1) == 114
print('9a: ', run(data))
assert run(ex1, part=2) == 2
print('9b: ', run(data, part=2))



