from aocd import data
import re

def run(data, part=1):
    lines = data.splitlines()
    dir_queue = [*lines[0]]
    nodes = {}
    for line in lines[2:]:
        (node, connections) = re.match('^(\w+) = \((.*)\)', line).groups()
        nodes[node] = connections.split(', ')
    
    # follow paths to end
    step = 0
    if (part==1):
        cur_nodes = ['AAA']
    else:
        cur_nodes = [x for x in nodes.keys() if x.endswith('A')]
    while True:
        dir = dir_queue.pop(0)
        dir_queue.append(dir)

        cur_nodes = [nodes[node][0 if dir=='L' else 1] for node in cur_nodes]
        step += 1
        if len([node for node in cur_nodes if node.endswith('Z')]) == len(cur_nodes):
            return step

ex1='''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''
ex2='''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''
ex3='''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''

assert run(ex1) == 2
assert run(ex2) == 6

print('8a: ', run(data))
assert run(ex3, part=2) == 6
print('8b: ', run(data, part=2))