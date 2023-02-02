from aocd import lines
import re

stacks = []
steps = []

def parse_line(line):
    if re.match('^[ 1-9]+$', line):
        return
    if re.match('^move', line):
        steps.append(line)
    idx = 0
    while idx > -1:
        idx = line.find('[',idx)
        if idx > -1:
            while len(stacks) <= idx // 4:
                stacks.append([])               
            stacks[idx // 4].insert(0, line[idx + 1])
            idx += 4

def parse(lines):
    global stacks, steps
    stacks = []
    steps = []
    for line in lines:
        parse_line(line)

def run_step(step, part=1):
    cnt, col1, col2 = [int(x) for x in re.match('move (\d+) from (\d) to (\d)', step).groups()]
    if part == 1:
        for x in range(0, cnt):
            val = stacks[col1 - 1].pop()
            stacks[col2 - 1].append(val)
    else:
        val = stacks[col1 - 1][-cnt:]
        stacks[col1 - 1] = stacks[col1 - 1][:-cnt]
        stacks[col2 - 1].extend(val)
    return

def run(part=1):
    for step in steps:
        run_step(step, part)
    result = ''
    for stack in stacks:
        result += stack.pop()
    return result

ex1 = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
parse(ex1.splitlines()); assert run() == 'CMZ'
parse(lines); print('5a: ', run())

parse(ex1.splitlines()); assert run(part = 2) == 'MCD'
parse(lines); print('5b: ', run(part = 2))
