from aocd import lines

def intersection(r1,r2):
    s1 = set(r1)
    s2 = set(r2)
    return list(s1.intersection(s2))[0]

def item_priority(item):
    common = ord(item)
    if common >= ord('a'):
        return common - ord('a') + 1
    return common - ord('A') + 27

def priority(line):
    l = int(len(line) / 2)
    return item_priority(intersection(line[:l],line[l:]))
    
def sum_priorities(lines):
    tot = 0
    for line in lines:
        tot += priority(line)
    return tot

def sum_badgepriorities(lines):
    it = iter(lines)
    tot = 0
    for sack in it:
        s1 = set(sack)
        s2 = set(next(it))
        s3 = set(next(it))
        common = list(s1.intersection(s2,s3))
        tot += item_priority(common[0])
    return tot


ex1 = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
assert sum_priorities(ex1.splitlines()) == 157
print('3a: ', sum_priorities(lines))

assert sum_badgepriorities(ex1.splitlines()) == 70
print('3b: ', sum_badgepriorities(lines))
