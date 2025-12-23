from aocd import data

def part1(data):
    rows = []
    total = 0
    for row in data.splitlines():
        rows.append(row.split())

    for col in range(len(rows[0])):
        op = rows[-1][col]
        val = 0 if op == '+' else 1
        for row in range(len(rows) - 1):
            if op == '+':
                val += int(rows[row][col])
            else:
                val *= int(rows[row][col])
        total += val
    return total

def part2(data):
    rows = []
    total = 0
    val = 0
    for row in data.splitlines():
        rows.append(row)
    cur_op = None
    for col in range(len(rows[0])):
        if rows[-1][col] in ('+', '*'):
            if val > 0:
                total += val
            cur_op = rows[-1][col]
            val = 0 if cur_op == '+' else 1
        # go through columns to generate numbers
        num_str = ''
        for row in range(len(rows) - 1):
            ch = rows[row][col]
            num_str += ch
        num_str = num_str.strip()
        if num_str:
            if cur_op == '+':
                val += int(num_str)
            else:
                val *= int(num_str)
    total += val
    return total

ex1='''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
'''

assert part1(ex1) == 4277556
print('6a: ', part1(data))
assert part2(ex1) == 3263827
print('6b: ', part2(data))