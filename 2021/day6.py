from aocd import lines
from collections import defaultdict

def count_fish(initial_fish, num_days = 80):
    school = defaultdict(int)
    for fish_age in map(int, initial_fish.split(',')):
        school[fish_age] += 1
    for day in range(0, num_days):
        new_school = defaultdict(int)
        new_school[8] = school[0]
        for age, cnt in school.items():
            if age == 0:
                new_school[6] += cnt
            else:
                new_school[age - 1] += cnt
        school = new_school
    return sum(school.values())

assert count_fish("3,4,3,1,2", 18) == 26
assert count_fish("3,4,3,1,2") == 5934
print('6a: ', count_fish(lines[0]))
print('6b: ', count_fish(lines[0], 256))
