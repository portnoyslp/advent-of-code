from aocd import data
import numpy as np
from scipy.spatial.distance import pdist,squareform

def run(data, num_cnxns):
    coords = []
    for line in data.splitlines():
        if not line:
            continue
        parts = line.split(',')
        coords.append((int(parts[0]), int(parts[1]), int(parts[2])))

    all_distances = pdist(coords, 'euclidean')
    distance_grid = squareform(all_distances)
    sorted_distances = np.sort(all_distances)
    circuits = []
    added_pairs = 0
    while added_pairs <= num_cnxns:
        short_dist = sorted_distances[0]
        i, j = np.where(distance_grid == short_dist)
        unique_pair = [(row.item(), col.item()) for row, col in zip(i, j) if row < col]

        # If a unique pair's coords already exists in one of the circuits, add
        # the coords to that circuit. Otherwise, add a circuit for this pair.
        added = False
        row, col = unique_pair[0]
        for circuit in circuits:
            if row in circuit or col in circuit:
                circuit.add(row)
                circuit.add(col)
                added = True
                break
        if not added:
            circuits.append(set([row, col]))
        added_pairs += 1

        # Remove first element of sorted_distances
        sorted_distances = sorted_distances[1:]

    # Get three largest circuits
    largest_circuits = sorted(circuits, key=lambda x: len(x), reverse=True)[:3]
    return np.prod([len(circuit) for circuit in largest_circuits])

def solve(data, num_cnxns, part=1):
    coords = []
    for line in data.splitlines():
        if not line:
            continue
        parts = line.split(',')
        coords.append((int(parts[0]), int(parts[1]), int(parts[2])))

    # Build a list of pairs of coords, reverse sorted by distance
    ncoords = len(coords)
    distances = []
    for c1 in range(ncoords):
        for c2 in range(c1+1, ncoords):
            dx = (coords[c1][0] - coords[c2][0]) ** 2
            dy = (coords[c1][1] - coords[c2][1]) ** 2
            dz = (coords[c1][2] - coords[c2][2]) ** 2
            distances.append([dx + dy + dz, [c1,c2]])
    distances.sort(reverse=True)

    # Initially all circuits are a single coord
    circuits = [{n} for n in range(ncoords)]
    def cfind(n):
        for i,circuit in enumerate(circuits):
            if n in circuit:
                return i
        return None

    n = num_cnxns
    while n > 0:
        n -= 1
        c1, c2 = distances.pop()[1]
        # Find the circuits these coords are in
        i1, i2 = cfind(c1), cfind(c2)
        if i1 != i2:
            # Merge circuits
            circuits[i1] = circuits[i1] | circuits[i2]
            del circuits[i2]
        if part == 2:
            # Keep going until only 1 circuit
            if len(circuits) == 1:
                break
            n += 1

    if part == 1:
        # Multiply length of 3 longest circuits
        circuits.sort(key=lambda c: len(c))
        return len(circuits.pop()) * len(circuits.pop()) * len(circuits.pop())
    else:
        # Multiply x coords of final joined pair
        return (coords[c1][0] * coords[c2][0])


ex1='''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
'''

# assert run(ex1, 10) == 40
# print('8a: ', run(data, 1000))

assert solve(ex1, 10) == 40
print('8a: ', solve(data, 1000))
assert solve(ex1, 10, part=2) == 25272
print('8b: ', solve(data, 1000, part=2))