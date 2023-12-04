from aocd import data
import re
import math

limits = {'red': 12, 'green': 13, 'blue': 14}

def play_games(data, part=1):
    sum_indices = 0
    sum_power = 0
    for game in data.splitlines():
        groups = re.match('Game (\d+): (.*)$', game).groups()
        game_num = int(groups[0])
        draws = groups[1].split('; ')
        add_index = True
        needed_cubes = {'red': 0, 'green': 0, 'blue': 0}
        for draw in draws:
            cubes = draw.split(', ')
            for cube in cubes:
                m = re.match('(?P<count>\d+) (?P<color>\w+)', cube)
                if limits[m['color']] < int(m['count']):
                    add_index = False
                needed_cubes[m['color']] = max(needed_cubes[m['color']], int(m['count']))
        if add_index: 
            sum_indices += game_num
        power = math.prod(needed_cubes.values())
        sum_power += power
    return sum_indices if part == 1 else sum_power
                

ex1 = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''
assert play_games(ex1) == 8
print('2a: ', play_games(data))
assert play_games(ex1, part=2) == 2286
print('2a: ', play_games(data, part=2))