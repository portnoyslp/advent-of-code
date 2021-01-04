import re
from aocd import data
import json

def find_nums(input_str):
    return sum(map(int, re.findall(r'-?\d+', input_str)))

assert find_nums('''[1,2,3]
{"a":2,"b":4}
[[3]]
{"a":{"b":4},"c":-1}
[]''') == 18
print('12a: ', find_nums(data))

def sum_nums(structure, ignore_red=False):
    if type(structure) is int:
        return structure
    if type(structure) is str:
        return 0
    if type(structure) is list:
        return sum(map(lambda x: sum_nums(x, ignore_red), structure))
    if ignore_red and 'red' in structure.values():
        return 0
    return sum(map(lambda x: sum_nums(x, ignore_red), structure.values()))


def parse_and_find_nums(input_str, ignore_red=False):
    struct = json.loads(input_str)
    return sum_nums(struct, ignore_red)

test_input = '''[[1,2,3],
[1,{"c":"red","b":2},3],
{"d":"red","e":[1,2,3,4],"f":5},
[1,"red",5],
[],
{}]'''
assert parse_and_find_nums(test_input) == 33
assert parse_and_find_nums(test_input, ignore_red=True) == 16
print('12b: ', parse_and_find_nums(data, ignore_red=True))
