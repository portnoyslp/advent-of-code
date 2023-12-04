from aocd import data
import re

def run(data):
    sum = 0
    for line in data.splitlines():
        match = re.match('Card +\d+: (.*) \| (.*)', line)
        wins = set([int(x) for x in match.group(1).split()])
        mine = [int(x) for x in match.group(2).split()]
        matches = [1 for x in mine if x in wins]
        num_matches = len(matches)
        if num_matches > 0:
          sum += pow(2, num_matches - 1)
    return sum

def part2(data):
    card_info = []
    for line in data.splitlines():
        match = re.match('Card +(\d+): (.*) \| (.*)', line)
        card = int(match.group(1))
        wins = set([int(x) for x in match.group(2).split()])
        mine = [int(x) for x in match.group(3).split()]
        matches = [1 for x in mine if x in wins]
        num_matches = len(matches)
        card_info.append([1, num_matches])

    for idx in range(len(card_info)):
        card_data = card_info[idx]
        [num_cards, num_matches] = card_data
        for i in range(num_matches):
            card_info[idx + i + 1][0] = card_info[idx + i + 1][0] + num_cards
    return sum([x[0] for x in card_info])

ex1='''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''

assert run(ex1) == 13
print('4a: ', run(data))
assert part2(ex1) == 30
print('4b: ', part2(data))