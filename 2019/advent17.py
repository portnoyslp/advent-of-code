from aocd import data
from intcode import Intcode

def get_ascii_str(input_str):
    intcode = Intcode(input_str)
    output = intcode.run_machine([])
    return ''.join(map(chr, output))

def find_crosses(input_str):
    input_array = input_str.splitlines()
    coords = []
    for yc in range(1, len(input_array) - 1):
        start = 0
        line = input_array[yc]
        while True:
            idx = line.find('###', start)
            if idx == -1:
                break
            if input_array[yc - 1][idx + 1] == '#' and input_array[yc + 1][idx + 1] == '#':
                coords.append( (yc, idx + 1) )
            start = idx + 1
    return coords

def answer(input_str):
    coords = find_crosses(get_ascii_str(input_str))
    return sum(map(lambda c: c[0] * c[1], coords))

print(f"{get_ascii_str(data)}")
print(f"17a => {answer(data)}")


def run_maze(input_str, maze_dirs):
    memory = list(map(int, input_str.split(',')))
    memory[0] = 2 # run mode
    input = [ord(c) for c in maze_dirs]
    robot = Intcode(memory)
    return robot.run_machine(input)


maze_dirs = '''A,B,B,C,C,A,B,B,C,A
R,4,R,12,R,10,L,12
L,12,R,4,R,12
L,12,L,8,R,10
n
'''
output = run_maze(data, maze_dirs)
print(f"17b: {run_maze(data, maze_dirs)}")
print (''.join(map(chr, output)))

