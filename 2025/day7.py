from aocd import data

def part1(data):
    rows = data.splitlines()
    splits = 0
    cur_cols = set()
    cur_cols.add(rows[0].index('S'))
    for row in range(1, len(rows)):
        next_cols = set()
        for c in cur_cols:
            if rows[row][c] == '^':
                next_cols.add(c-1)
                next_cols.add(c+1)
                splits += 1
            else:
                next_cols.add(c)
        cur_cols = next_cols
    return splits

def part2(data):
    rows = data.splitlines()
    cur_cols = dict()
    cur_cols[rows[0].index('S')] = 1
    for row in range(1, len(rows)):
        next_cols = cur_cols.copy()
        for c, count in cur_cols.items():
            if rows[row][c] == '^':
                next_cols[c] = 0
                next_cols[c-1] = next_cols.get(c-1, 0) + count
                next_cols[c+1] = next_cols.get(c+1, 0) + count
        cur_cols = next_cols
    return sum(cur_cols.values())


ex1='''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
'''

assert part1(ex1) == 21
print('7a: ', part1(data))
assert part2(ex1) == 40
print('7b: ', part2(data))