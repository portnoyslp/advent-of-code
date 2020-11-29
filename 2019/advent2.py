#!/usr/bin/python

basememory = list(map(int, raw_input().split(',')))
memory = []
iptr = 0


def add():
    global iptr
    idx1 = memory[iptr+1]
    idx2 = memory[iptr+2]
    outputIdx = memory[iptr+3]
    iptr += 4
    memory[outputIdx] = memory[idx1] + memory[idx2]

def mult():
    global iptr
    idx1 = memory[iptr+1]
    idx2 = memory[iptr+2]
    outputIdx = memory[iptr+3]
    iptr += 4
    memory[outputIdx] = memory[idx1] * memory[idx2]

def stop():
    return 99

opcodes = {
    1: add,
    2: mult,
    99: stop
    }

def processOpcode():
    opcode = memory[iptr]
    opcodes[opcode]()
    return 99 if opcode == 99 else 0

def runWithValues(a, b):
    global iptr
    global memory
    iptr = 0
    memory = list(basememory)
    memory[1] = a
    memory[2] = b
    while (processOpcode() != 99):
      continue
    return memory[0]

for a in range(99):
    for b in range(99):
        result = runWithValues(a,b)
        if (result == 19690720):
          print "{},{} ({}) => {}".format(a,b,100*a+b,result)
          break



