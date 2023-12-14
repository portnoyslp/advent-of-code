from aocd import data

def run(data, part=1):
    patterns = data.split('\n\n')
    total = 0
    for pattern in patterns:
        rows = pattern.splitlines()
        reflections = get_reflections(rows)
        if part == 2:
            # de-smudge every cell until we get a different reflection
            stop_running = False
            for yp, row in enumerate(rows):
                if stop_running:
                    break
                old_row = row
                for xp, ch in enumerate(row):
                    rows[yp] = old_row[:xp] + ('.' if ch == '#' else '#') + old_row[xp+1:]
                    new_reflections = get_reflections(rows)
                    if new_reflections and new_reflections != reflections:
                        if reflections[0] in new_reflections: new_reflections.remove(reflections[0]) # old should only be one
                        reflections = new_reflections
                        stop_running = True
                        break
                    rows[yp] = old_row
            if not stop_running:
                print('Didn''t find a new reflection for:\n' + pattern)
        total += sum(reflections)
    return total

def get_reflections(rows):
    reflections = []
    reflections.extend(map(lambda x: 100 * x, horizontal_pivots(rows)))
    reflections.extend(vertical_pivots(rows))
    return reflections

def horizontal_pivots(rows):
    return find_pivots(rows)

def vertical_pivots(rows):
    rotated = list(map(lambda x: ''.join(x), zip(*rows[::-1])))
    return find_pivots(rotated)

def find_pivots(rows):
    pivots = []
    for idx, row in enumerate(rows[:-1]):
        if row == rows[idx + 1]:
            # two rows (idx and idx + 1) that are the same; double check that the pattern repeats.
            patternMatching = True
            for y in range(idx + 2, len(rows)):
                if (2*idx - y + 1) < 0:
                    break
                if rows[y] != rows[2*idx - y + 1]:
                    patternMatching = False
                    break
            if patternMatching:
                pivots.append(idx + 1)
    return pivots

ex1='''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''

assert run(ex1) == 405
print('13a: ', run(data))
assert run(ex1, part=2) == 400
print('13b: ', run(data, part=2))