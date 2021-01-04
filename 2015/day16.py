from aocd import data
import re

known_vals = {}
def parse_knowns(known_str):
    for line in known_str.splitlines():
        key, val = re.match(r'(\w+): (\d+)', line).groups()
        known_vals[key] = int(val)


def find_matches(input_str, retroencabulator=1):
    for line in input_str.splitlines():
        aunt, props = re.match(r'\w+ (\d+): (.*)$', line).groups()
        match = True
        for prop in props.split(', '):
            if not matched(prop, retroencabulator):
                match = False
                break
        if match:
            return aunt


def matched(prop, retroencabulator_version):
    name = prop[:prop.find(':')]
    val = int(prop[prop.find(':') + 1:])
    if retroencabulator_version == 2 and name in ('cats', 'trees'):
        return known_vals[name] < val
    if retroencabulator_version == 2 and name in ('pomeranians', 'goldfish'):
        return known_vals[name] > val
    if name in known_vals and known_vals[name] != val:
        return False
    return True


knowns = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''
parse_knowns(knowns)
print('16a: ', find_matches(data))
print('16b: ', find_matches(data, retroencabulator=2))
