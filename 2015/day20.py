from math import sqrt, floor
from itertools import count
from collections import defaultdict


def sum_divisors(n):
    divs = []
    for x in range(1, floor(sqrt(n))):
        if n % x == 0:
            divs.extend([x, n // x])
    return sum(divs)


def first_above_prev(target):
    for x in count(floor(sqrt(target // 10))):
        if sum_divisors(x) * 10 > target:
            return x


def first_above(target, mult=10, stops=None):
    house = defaultdict(int)
    for i in range(1, target // mult):
        limit = (target // mult) if stops is None else stops * i + 1
        for j in range(i, limit, i):
            house[j] += i * mult
    return min([k for k in house.keys() if house[k] >= target])


print('20a: ', first_above(29000000))
print('20b: ', first_above(29000000, mult=11, stops=50))
