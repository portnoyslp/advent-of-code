from aocd import data

def area(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

def run(data, part=1):
    coords = []
    for line in data.splitlines():
        parts = line.split(',')
        coords.append((int(parts[0]), int(parts[1])))

    max_area = 0
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            if area(coords[i], coords[j]) > max_area:
                max_area = area(coords[i], coords[j])
    return max_area



ex1='''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
'''

assert run(ex1) == 50
print('9a: ', run(data))
assert run(ex1, part=2) == 24
print('9b: ', run(data, part=2))