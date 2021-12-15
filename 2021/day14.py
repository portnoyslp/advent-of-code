from aocd import lines
from collections import defaultdict

def process_steps(input_lines, steps=10):
    element_count = defaultdict(int)
    pair_count = defaultdict(int)
    rules = {}

    initial_input = input_lines[0]
    for line in input_lines[2:]:
        (f,t) = line.split(' -> ')
        rules[f] = t
    for idx,x in enumerate(initial_input):
        element_count[x] += 1
        if idx > 0:
            pair_count[initial_input[idx-1:idx+1]] += 1
    
    for step in range(0,steps):
        update = pair_count.copy()
        for key,val in pair_count.items():
            result = rules[key]
            if result:
                update[key] -= val
                update[key[0] + result] += val
                update[result + key[1]] += val
                element_count[result] += val
        pair_count = update
    
    counts = sorted(element_count.values())
    return counts[-1] - counts[0]


test="""NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

assert(process_steps(test.splitlines()) == 1588)
print('14a: ', process_steps(lines))

assert(process_steps(test.splitlines(), 40) == 2188189693529)
print('14b: ', process_steps(lines, 40))