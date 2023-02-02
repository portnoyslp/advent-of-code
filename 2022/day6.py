from aocd import lines
from collections import defaultdict

def find_marker(line, count=4):
    buckets = defaultdict(int)
    for idx,ch in enumerate(line):
        buckets[ch] += 1
        if idx >= count:
            buckets[line[idx - count]] -= 1
            full_buckets = sum(1 for x in buckets.values() if x > 0)
            if full_buckets == count:
                return idx + 1;

assert find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
assert find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11
print('6a: ', find_marker(lines[0]))

assert find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
assert find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
assert find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26
print('6b: ', find_marker(lines[0], 14))
