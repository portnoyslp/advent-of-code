from aocd import data

def count_valid_ingredients(data):
    ranges = []
    ingredients = []
    for line in data.splitlines():
        if not line:
            continue
        if '-' in line:
            parts = line.split('-')
            ranges.append((int(parts[0]), int(parts[1])))
        else:
            ingredients.append(int(line))
    valid_ingredients = set()
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                valid_ingredients.add(ingredient)
                break
        if ingredient in valid_ingredients:
            continue
    return len(valid_ingredients)

def merge_intervals(intervals):
    """
    Merges a list of intervals (ranges) into a list of non-overlapping intervals.
    Assumes the input list of intervals is already sorted by the start of each interval.
    """
    if not intervals:
        return []

    merged = []
    # Start with the first interval
    for current_start, current_end in intervals:
        # If the merged list is empty, or the current interval doesn't overlap
        # with the last one in the merged list, simply append it.
        if not merged or current_start > merged[-1][1]:
            merged.append([current_start, current_end])
        else:
            # Otherwise, there is an overlap, so merge the current interval
            # with the last one by updating the end point if necessary.
            merged[-1][1] = max(merged[-1][1], current_end)
            
    return merged

def add_and_merge(existing_ranges, new_range):
    """
    Inserts a new range into a sorted list of ranges and merges overlaps.
    """
    # Combine all ranges first. Sorting is a necessary pre-step for the merge algorithm.
    all_ranges = existing_ranges + [new_range]
    all_ranges.sort(key=lambda x: x[0])
    
    # Use the main merge function to resolve overlaps
    return merge_intervals(all_ranges)

def all_valid_ingredients(data):
    ranges = []
    for line in data.splitlines():
        if not line:
            break
        if '-' in line:
            parts = line.split('-')
            ranges = add_and_merge(ranges, (int(parts[0]), int(parts[1])))
    
    num_valid_ingredients = 0
    for range_start, range_end in ranges:
        num_valid_ingredients += (range_end - range_start + 1)
    return num_valid_ingredients

ex1='''3-5
10-14
16-20
12-18

1
5
8
11
17
32
'''

assert count_valid_ingredients(ex1) == 3
print('5a: ', count_valid_ingredients(data))
assert all_valid_ingredients(ex1) == 14
print('5b: ', all_valid_ingredients(data)) 
