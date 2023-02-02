from aocd import lines

def cal_counts(lines):
    sum = 0
    result = []
    for line in lines:
        if line == '':
            result.append(sum)
            sum = 0
        else:
            sum += int(line)
    result.append(sum)
    return result

def p1(lines):
    return max(cal_counts(lines))
def p2(lines):
    cals = cal_counts(lines)
    cals.sort(reverse = True)
    return cals[0] + cals[1] + cals[2]

ex1 = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''

assert p1(ex1.splitlines()) == 24000
print('1a: ', p1(lines))

assert p2(ex1.splitlines()) == 45000
print('1b: ', p2(lines))

