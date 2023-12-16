from aocd import data
from functools import reduce
import re

def run(data, part=1):
    cmds = data.rstrip().split(',')
    if part == 1:
        return sum([hash(x) for x in cmds])
    # make a poor man's hashtable, with an 256-entry array of lists.
    hashmap = []
    for i in range(256): hashmap.append([])
    for cmd in cmds:
        label, op, val = re.match('^([a-z]+)(=|-)(\d*)', cmd).groups()
        idx = hash(label)
        boxes = hashmap[idx]
        if op == '=':
            pair = (label, int(val))
            box_idx = index_of_tuple(boxes, pair)
            if box_idx != None:
                # replace
                boxes[box_idx] = pair
            else:
                boxes.append(pair)
            hashmap[idx] = boxes
        else:
            # remove mapping
            hashmap[idx] = [b for b in boxes if b[0] != label]
        # print(f'After "{cmd}":')
        # print_map(hashmap)
    total = 0
    for idx, boxes in enumerate(hashmap):
        for box_idx, box in enumerate(boxes):
            focus_power = (idx + 1) * (box_idx+1) * box[1]
            total += focus_power
    return total

def print_map(hashmap):
    for idx,boxes in enumerate(hashmap):
        if len(boxes) > 0:
            print(f'Box {idx}: ' + ' '.join([f'[{box[0]} {box[1]}]' for box in boxes]))



def index_of_tuple(lst, tup):
    for idx,t in enumerate(lst):
        if t[0] == tup[0]:
            return idx
    return None



def hash(str):
    return reduce(lambda a,b: ((a + ord(b))*17)%256, str, 0)


ex1='''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''

assert run(ex1) == 1320
print('15a: ', run(data))
assert run(ex1, part=2) == 145
print('15b: ', run(data, part=2))