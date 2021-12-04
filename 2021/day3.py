from aocd import lines
from collections import defaultdict

def power_consumption(lines):
    bit_counts = []
    for idx in range(0, len(lines[0])):
        bit_counts.append(bit_count_dict(lines, idx))
    gamma = ''
    epsilon = ''
    for bit in bit_counts:
        gamma += '0' if bit['0'] > bit['1'] else '1'
        epsilon += '1' if bit['0'] > bit['1'] else '0'
    return int(gamma,2) * int(epsilon, 2)

def bit_count_dict(lines, idx):
    counts = defaultdict(int)
    for line in lines:
        bit = line[idx]
        counts[bit] += 1
    return counts


test = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

assert power_consumption(test.splitlines()) == 198
print('3a: ', power_consumption(lines))

def life_support_rating(lines):
    oxygen_input = lines
    for idx in range(0,len(lines[0])):
        bit_counts = bit_count_dict(oxygen_input, idx)
        most_common = '0' if bit_counts['0'] > bit_counts['1'] else '1'
        new_oxygen_input = []
        for oxygen in oxygen_input:
            if oxygen[idx] == most_common:
                new_oxygen_input.append(oxygen)
        oxygen_input = new_oxygen_input
        if len(oxygen_input) == 1:
            break;

    carbon_dioxide_input = lines
    for idx in range(0,len(lines[0])):
        bit_counts = bit_count_dict(carbon_dioxide_input, idx)
        least_common = '0' if bit_counts['0'] <= bit_counts['1'] else '1'
        new_carbon_dioxide_input = []
        for carbon_dioxide in carbon_dioxide_input:
            if carbon_dioxide[idx] == least_common:
                new_carbon_dioxide_input.append(carbon_dioxide)
        carbon_dioxide_input = new_carbon_dioxide_input
        if len(carbon_dioxide_input) == 1:
            break;
    
    return int(oxygen_input[0], 2) * int(carbon_dioxide_input[0],2)

assert life_support_rating(test.splitlines()) == 230
print('3b: ', life_support_rating(lines))

        

