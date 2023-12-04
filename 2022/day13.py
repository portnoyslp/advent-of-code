from aocd import data
from functools import cmp_to_key

def ordered_packets(data):
    sum_idx = 0
    for idx, pair in enumerate(data.rstrip().split('\n\n')):
        lists = [eval(l) for l in pair.split('\n')]
        if compare(lists[0], lists[1]) < 0:
            sum_idx += idx + 1
    return sum_idx

def decoder_key(data):
    lists = [eval(l) for l in data.splitlines() if l != '']
    lists.append([[2]])
    lists.append([[6]])
    lists.sort(key=cmp_to_key(compare))
    
    idx1 = lists.index([[2]]) + 1
    idx2 = lists.index([[6]]) + 1
    return idx1 * idx2

indent = 0
def compare(left, right):
    global indent
    # print ('  ' * indent, 'Compare {} vs {}'.format(left, right))
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if left > right:
            return 1
        return 0

    if isinstance(left, list) and isinstance(right, list):
        for idx in range(min(len(left), len(right))):
            indent += 1
            c = compare(left[idx], right[idx])
            indent -= 1
            if c != 0:
                return c
        return compare(len(left), len(right))
    
    if isinstance(left, int):
        return compare([left], right)
    return compare(left, [right])

ex1='''[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''

assert ordered_packets(ex1) == 13
print('13a: ', ordered_packets(data))
assert decoder_key(ex1) == 140
print('13b: ', decoder_key(data))