from aocd import data
import itertools

containers = list(map(int, data.splitlines()))
total_found = 0
found_by_cnt = {}
for cnt in range(1, len(containers) + 1):
    found = 0
    for sizes in itertools.combinations(containers, cnt):
        if sum(sizes) == 150:
            found += 1
    total_found += found
    if found > 0:
        found_by_cnt[cnt] = found
print(f'17a: {total_found}')
print('17b: ', found_by_cnt[min(found_by_cnt.keys())] )