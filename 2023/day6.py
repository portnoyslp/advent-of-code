from aocd import data
import re
from math import prod

def run(data, part=1):
    lines = data.splitlines()
    timelist = re.match('.*: ([ \d]+)', lines[0]).group(1)
    distlist = re.match('.*: ([ \d]+)', lines[1]).group(1)
    
    if part == 1:
        times = [int(x) for x in timelist.split()]
        distances = [int(x) for x in distlist.split()]

        num_matches = []
        for idx in range(len(times)):
            time = times[idx]
            dist = distances[idx]
            num_matches.append(num_ways_to_beat(time, dist))
        return prod(num_matches)
    
    time = int(timelist.replace(' ', ''))
    dist = int(distlist.replace(' ', ''))
    return num_ways_to_beat(time, dist)


def num_ways_to_beat(time, dist):
    # use binary search to find first instance where x*(time - x) > dist
    low = 0
    high = time // 2;
    while low < high:
        mid = (low + high) // 2
        cur_dist = mid * (time - mid)
        if cur_dist > dist:
            high = mid - 1                
        else:
            low = mid + 1
    # if low is too low, adjust.
    if (low*(time - low) <= dist):
        low += 1
    return time + 1 - low * 2


ex1='''Time:      7  15   30
Distance:  9  40  200
'''

assert run(ex1) == 288
print('6a: ', run(data))
assert run(ex1, part=2) == 71503
print('6b: ', run(data, part=2))
