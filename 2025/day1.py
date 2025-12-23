from aocd import data

def count_zeroes(input_data: str, part=1) -> int:
    lines = input_data.splitlines()
    zeroes = 0
    cur_pos = 50
    for line in lines:
        dir = line[0]
        num = int(line[1:])

        (rotations, remainder) = divmod(num, 100)

        if dir == 'L':
            new_pos = cur_pos - remainder
        elif dir == 'R':
            new_pos = cur_pos + remainder
        
        zero_passed = int(cur_pos != 0 and not (0 < new_pos < 100))
        zeroes += rotations + zero_passed if part == 2 else (1 if new_pos % 100 == 0 else 0)
        
        cur_pos = new_pos % 100
    
    return zeroes

ex1 = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''
assert count_zeroes(ex1) == 3
print('1a: ', count_zeroes(data))
assert count_zeroes(ex1, part=2) == 6
print('1b: ', count_zeroes(data, part=2))

