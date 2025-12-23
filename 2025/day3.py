from aocd import data
from functools import lru_cache

@lru_cache(maxsize=None)
def best_joltage(bank, size):
    if not bank or size == 0 or size > len(bank):
        return 0
    joltage_with_last = 10 * best_joltage(bank[:-1], size - 1) + int(bank[-1])
    joltage_without_last = best_joltage(bank[:-1], size)
    return max(joltage_with_last, joltage_without_last)

def run(data, part=1):
    sum_joltage = 0
    for line in data.splitlines():
        sum_joltage += best_joltage(line, 2 if part == 1 else 12)
    return sum_joltage

ex1='''987654321111111
811111111111119
234234234234278
818181911112111
'''

assert run(ex1) == 357
print('3a: ', run(data))
assert run(ex1, 2) == 3121910778619
print('3b: ', run(data, 2))