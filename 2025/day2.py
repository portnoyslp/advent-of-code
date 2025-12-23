from aocd import data

def repeating_id(id_str: str, num_groups) -> bool:
    if len(id_str) % num_groups != 0:
        return False
    sublen = len(id_str) // num_groups

    for i in range(sublen):
        for j in range(1, num_groups):
            if id_str[i] != id_str[i + j * sublen]:
                return False
    return True

def invalid_id(id_str: str, part=1) -> bool:
    if part == 1:
        return repeating_id(id_str, 2)
    for num_groups in range(2, len(id_str) + 1):
        if repeating_id(id_str, num_groups):
            return True
    return False

def run(data, part=1):
    id_ranges = data.split(',')
    invalid_id_sum = 0
    for id_range in id_ranges:
        (start, end) = id_range.split('-')
        for id in range(int(start), int(end) + 1):
            id_str = str(id)
            invalid_id_sum += id if invalid_id(id_str, part) else 0

    return invalid_id_sum

ex1='''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
'''

assert run(ex1) == 1227775554
print('2a: ', run(data))
assert run(ex1, 2) == 4174379265
print('2b: ', run(data, 2))