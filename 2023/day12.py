from aocd import data
from functools import lru_cache

def run(data, part=1):
    total = 0
    for line in data.splitlines():
        (pattern, expected) = line.split(' ')
        if part == 2:
            pattern = (('?' + pattern) * 5)[1:]
        expected = tuple(map(int, expected.split(',')))
        if part == 2:
            expected = expected * 5
        cnt = array_count(pattern, expected, False)
        total += cnt
    return total

@lru_cache(maxsize=None)
def array_count(pattern, expected, in_lava):
    dec_first = lambda a: (a[0] - 1,) + a[1:]
    if not expected:
        return 0 if '#' in pattern else 1
    if not pattern:
        return 0 if sum(expected) else 1
    if expected[0] == 0:
        return array_count(pattern[1:], expected[1:], False) if pattern[0] in '?.' else 0
    if in_lava:
        return array_count(pattern[1:], dec_first(expected), True) if pattern[0] in '?#' else 0
    if pattern[0] == '#':
        return array_count(pattern[1:], dec_first(expected), True)
    if pattern[0] == '.':
        return array_count(pattern[1:], expected, False)
    return array_count(pattern[1:], expected, False) + array_count(pattern[1:], dec_first(expected), True)


ex1='''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''

assert run(ex1) == 21
print('12a: ', run(data))
assert run(ex1, part=2) == 525152
print('12b: ', run(data, part=2))