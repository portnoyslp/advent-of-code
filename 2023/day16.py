from aocd import data

def run(data):
    return 0

ex1='''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''

assert run(ex1) == 46
print('16a: ', run(data))