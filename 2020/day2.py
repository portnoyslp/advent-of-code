import re
from aocd import data

def count_valid_passwords(input):
    ok_words = 0
    for line in input.splitlines():
        if valid_password1(line):
            ok_words += 1
    return ok_words


def valid_password1(line):
    match = re.match(r'(\d+)-(\d+) (.): (.+)', line)
    if match is None:
        return False
    low, high, needed_char, pw = match.groups()
    count = pw.count(needed_char)
    return int(low) <= count <= int(high)


def valid_password2(line):
    match = re.match(r'(\d+)-(\d+) (.): (.+)', line)
    if match is None:
        return False
    pos1, pos2, needed_char, pw = match.groups()
    chars = [pw[i - 1] for i in [int(pos1), int(pos2)]]
    return chars.count(needed_char) == 1


def count_valid_passwords2(input):
    ok_words = 0
    for line in input.splitlines():
        if valid_password2(line):
            ok_words += 1
    return ok_words


test_input = '''
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''
assert count_valid_passwords(test_input) == 2
print(f"2a: {count_valid_passwords(data)}")

assert count_valid_passwords2(test_input) == 1
print(f"2b: {count_valid_passwords2(data)}")
