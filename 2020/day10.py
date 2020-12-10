from aocd import data
from functools import lru_cache


def mult_differences(input):
    adapters = adapter_list(input)
    adapters.append(adapters[-1] + 3)
    count1 = count3 = 0
    start_voltage = 0
    for adapter in adapters:
        if adapter - start_voltage == 1:
            count1 += 1
        elif adapter - start_voltage == 3:
            count3 += 1
        start_voltage = adapter
    return count1 * count3


def adapter_list(input):
    adapters = [int(x) for x in input.splitlines()]
    adapters.sort()
    return adapters


test_input1 = '''16
10
15
5
1
11
7
19
6
12
4'''

test_input2 = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''

assert mult_differences(test_input1) == 35
assert mult_differences(test_input2) == 220
print('10a: ', mult_differences(data))


def count_arrangements(input):
    all_adapters = adapter_list(input)
    out_joltage = all_adapters[-1] + 3

    @lru_cache(maxsize=None)
    def helper(in_joltage, adapters):
        if len(adapters) == 0:
            return 1 if out_joltage - in_joltage <= 3 else 0
        if adapters[0] - in_joltage > 3:
            return 0
        # Add together the arrangements without this adapter, and those with:
        remaining_adapters = tuple(adapters[1:])
        return helper(in_joltage, remaining_adapters) + helper(adapters[0], remaining_adapters)

    return helper(0, tuple(all_adapters))


assert count_arrangements(test_input1) == 8
assert count_arrangements(test_input2) == 19208
print('10b: ', count_arrangements(data))
