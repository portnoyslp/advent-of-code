from aocd import data
import re

mapchain = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']


def run(data):
    mappings = {}
    seeds = parse_data(data, mappings)
    min_val = 1000000000
    for seed in seeds:
        val = seed_to_location(mappings, seed)
        if val < min_val:
          min_val = val
   
    return min_val

def part2(data):
    mappings = {}
    seeds = parse_data(data, mappings)
    # Seeds are actually list pairs:
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append( (seeds[i], seeds[i] + seeds[i+1] - 1 ) )

    min_location = 1000000000
    val_ranges = seed_range_to_locations(mappings, seed_ranges)
    val_ranges.sort(key=lambda x: x[0])
    min_location = val_ranges[0][0]
    return min_location

def seed_to_location(mappings, seed):
    val = seed
    for chain in mapchain:
        val = range_map(mappings[chain], val)
    return val

def seed_range_to_locations(mappings, seed_ranges):
    ranges = seed_ranges
    for chain in mapchain:
        ranges = map_ranges(mappings[chain], ranges)
    return ranges

def parse_data(data, mappings):
    sections = data.split('\n\n')
    for section in sections:
        if 'seeds:' in section:
            seeds = [int(x) for x in re.match('^seeds: (.+)', section).group(1).split()]
            continue
        
        lines = section.splitlines()
        mapname = lines[0].split()[0]
        mapping = {}
        for line in lines[1:]:
            nums = [int(x) for x in line.split()]
            mapping[nums[1]] = (nums[0], nums[2])
        mappings[mapname] = mapping
    return seeds

# looks up a key from given map that goes from tuples start -> (target, dist), 
# and maps the values from the target so that they match.
def range_map(map, request):
    for k in map.keys():
        if k <= request < k + map[k][1]:
            return map[k][0] + (request - k)
    # values that aren't in map are unchanged.
    return request

# maps a provided range to a set of ranges when going through the map.
def map_range(map, request_range):
    output = []
    used_subranges = []
    for k in map.keys():
        key_range = (k, k + map[k][1] - 1)
        if request_range[1] < key_range[0] or request_range[0] > key_range[1]:
            # no overlap
            continue
        updated_range = (max(key_range[0], request_range[0]), min(key_range[1], request_range[1]))
        used_subranges.append(updated_range)
        output.append( (map[k][0] + (updated_range[0] - k), map[k][0] + (updated_range[1] - k)) )
    if len(output) == 0:
        # return range unmodified
        return [request_range]

    # Any values in range that weren't mapped are sent through unchanged.
    used_subranges.sort(key=lambda x: x[0])
    ranges_to_add = []
    if used_subranges[0][0] > request_range[0]:
        ranges_to_add.append(  (request_range[0], used_subranges[0][0] - 1) )
    for idx in range(1, len(used_subranges)):
        if used_subranges[idx-1][1] < used_subranges[idx][0] - 1:
            ranges_to_add.append( (used_subranges[idx-1][1] + 1, used_subranges[idx][0] - 1) )
    if used_subranges[-1][1] < request_range[1]:
        ranges_to_add.append( (used_subranges[-1][1] + 1, request_range[1]) ) 
    output.extend(ranges_to_add)
    return output

def map_ranges(map, request_ranges):
    output = []
    for range in request_ranges:
        new_ranges = map_range(map, range)
        output.extend(new_ranges)
    output.sort(key = lambda x: x[0])
    return output



ex1='''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''

assert run(ex1) == 35
print('5a: ', run(data))
assert part2(ex1) == 46
print('5b: ', part2(data))