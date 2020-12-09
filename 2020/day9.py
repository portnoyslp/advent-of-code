from aocd import data


def check_subset(subset, target):
    subset = set(subset)
    for val in subset:
        if target - val in subset and target != 2 * val:
            return True
    return False


def find_missing_with_preamble(input, preamble_width):
    stream = [int(x) for x in input.splitlines()]
    for idx in range(preamble_width, len(stream)):
        if not check_subset(stream[idx - preamble_width:idx], stream[idx]):
            return stream[idx]
    return 'No bad element found'


test_input = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
'''
assert find_missing_with_preamble(test_input, 5) == 127

print('9a: ', find_missing_with_preamble(data, 25))


def find_encryption_weakness(input, preamble_width):
    stream = [int(x) for x in input.splitlines()]
    invalid_num = find_missing_with_preamble(input, preamble_width)
    contiguous_digits = []
    contiguous_sum = 0
    cur_idx = 0
    while contiguous_sum != invalid_num:
        # If the current contiguous_sum is less than the target, add a digit onto the end
        # If it's greater than the target, take one off the start
        if contiguous_sum < invalid_num:
            val = stream[cur_idx]
            contiguous_digits.append(val)
            contiguous_sum += val
            cur_idx += 1
        else:
            val = contiguous_digits.pop(0)
            contiguous_sum -= val
    contiguous_digits.sort()
    return contiguous_digits[0] + contiguous_digits[-1]


assert find_encryption_weakness(test_input, 5) == 62
print('9b: ', find_encryption_weakness(data, 25))
