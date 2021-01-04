from aocd import data
import re

def count_decode(x):
    code_chars = 0
    str_chars = 0
    while len(x) != 0:
        inc = (0,0)
        if re.match(r"\\\\", x) or re.match(r'\\"', x):
            inc = (2,1)
        elif re.match(r'\\x[0-9a-f][0-9a-f]', x):
           inc = (4,1)
        elif re.match(r'"', x):
            inc = (1,0)
        else:
            inc = (1,1)
        x = x[inc[0]:]
        code_chars += inc[0]
        str_chars += inc[1]
    return code_chars, str_chars

def count_all_decode(input_str):
    count = (0,0)
    for line in input_str.splitlines():
        inc = count_decode(line)
        count = tuple(map(sum, zip(count, inc)))
    return count[0] - count[1]

def count_encode(x):
    code_chars = 0
    str_chars = 0
    while len(x) != 0:
        inc = (0,0)
        if x[0] == '"' or x[0] == '\\':
            code_chars += 2
        else:
            code_chars += 1
        str_chars +=1
        x = x[1:]
    # add two for surrounding double quotes
    return code_chars + 2, str_chars

def count_all_encode(input_str):
    count = (0,0)
    for line in input_str.splitlines():
        inc = count_encode(line)
        count = tuple(map(sum, zip(count, inc)))
    return count[0] - count[1]


test_input = '''""
"abc"
"aaa\\"aaa"
"\\x27"'''
assert count_all_decode(test_input) == 12
print('8a: ', count_all_decode(data))

assert count_all_encode(test_input) == 19
print('8b: ', count_all_encode(data))