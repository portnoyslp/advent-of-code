from aocd import data


def count_all_yes(group):
    people = map(set, group.split('\n'))
    all_yes = list(set.intersection(*people))
    return len(all_yes)


def count_any_yes(group):
    return len(set(''.join(group.split('\n'))))


def sum_counts(input):
    return sum([count_any_yes(group) for group in input.split('\n\n')])


def sum_counts_6b(input):
    return sum([count_all_yes(group) for group in input.split('\n\n')])


test_input = '''abc

a
b
c

ab
ac

a
a
a
a

b'''
assert sum_counts(test_input) == 11

print(f'6a: {sum_counts(data)}')

assert sum_counts_6b(test_input) == 6
print(f'6b: {sum_counts_6b(data)}')
