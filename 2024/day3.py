from aocd import data
import re

def sum_muls(data):
    result = 0
    for match in re.findall(r'mul\((\d+),(\d+)\)', data):
        result += int(match[0]) * int(match[1])
    return result

ex1 = '''xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''
assert sum_muls(ex1) == 161
print('3a: ', sum_muls(data))

def sum_enabled_muls(data):
    result = 0
    enabled = True
    for match in re.findall(r'(do\(\)|don\'t\(\)|mul\((\d+),(\d+)\))', data):
        if match[0] == 'do()':
            enabled = True
        elif match[0] == 'don\'t()':
            enabled = False
        else:
            if (enabled):
                result += int(match[1]) * int(match[2])
    return result


ex2 = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''
assert sum_enabled_muls(ex2) == 48
print('3b: ', sum_enabled_muls(data))
