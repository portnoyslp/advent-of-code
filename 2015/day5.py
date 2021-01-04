from aocd import data
import re


def check_nice(s):
    return re.match(r'.*[aeiou].*[aeiou].*[aeiou]', s) and re.match(r'.*(.)\1', s) and not re.match(r'.*(ab|cd|pq|xy)', s)


assert check_nice('ugknbfddgicrmopn')
assert check_nice('aaa')
assert not check_nice('jchzalrnumimnmhp')
assert not check_nice('haegwjzuvuyypxyu')
assert not check_nice('dvszwmarrgswjxmb')
print('5a: ', [check_nice(s) for s in data.splitlines()].count(True))

def check_nice2(s):
    return bool(re.match(r'.*(..).*\1', s) and re.match(r'.*(.).\1', s))

assert check_nice2('qjhvhtzxzqqjkmpb')
assert check_nice2('xxyxx')
assert not check_nice2('uurcxstgmygtbstg')
assert not check_nice2('ieodomkazucvgmuy')
print('5b: ', [check_nice2(s) for s in data.splitlines()].count(True))