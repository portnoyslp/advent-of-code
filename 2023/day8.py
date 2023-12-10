from aocd import data
import math
from functools import reduce
import re

nodes = {}

def run(data, part=1):
    global nodes
    nodes.clear()
    lines = data.splitlines()
    dir_queue = [*lines[0]]
    for line in lines[2:]:
        (node, connections) = re.match('^(\w+) = \((.*)\)', line).groups()
        nodes[node] = connections.split(', ')
    
    # follow paths to end
    if (part==1):
        cur_node = 'AAA'
        return steps_to_end(dir_queue, cur_node)[0]

    cur_nodes = [x for x in nodes.keys() if x.endswith('A')]
    # find loops and use LCM?
    output_loop_lengths = []
    saved_dir_queue = list(dir_queue)
    for start_node in cur_nodes:
        dir_queue = list(saved_dir_queue)
        # count both the steps to the end, and then the steps to reach the next end
        (start_steps, end_node, dir_queue) = steps_to_end(dir_queue, start_node)
        (next_steps, end_node_2, dir_queue) = steps_to_end(dir_queue, end_node)
        if end_node == end_node_2:
            # we have a loop. LCM is next_steps.
            output_loop_lengths.append( (start_steps, next_steps) )
        else:
            print("Not sure what to do: '" + start_node + "' gives weird loops", (start_steps, next_steps), "to", (end_node, end_node_2))
    lcm_all = reduce(math.lcm, [x[1] for x in output_loop_lengths])
    return lcm_all + (output_loop_lengths[0][1] - output_loop_lengths[0][0])




def steps_to_end(dir_queue, cur_node):
    step = 0
    while True:
        dir = dir_queue.pop(0)
        dir_queue.append(dir)

        cur_node = nodes[cur_node][0 if dir=='L' else 1]
        step += 1
        if cur_node.endswith('Z'):
            return (step, cur_node, dir_queue)
        


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