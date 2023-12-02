from aocd import data
import numpy as np

def count_visible(data):
    rows = data.splitlines()
    int_list = [list(map(int, [x for x in row])) for row in rows]
    trees = np.array(int_list)
    num_visible = 0
    for iy, ix in np.ndindex(trees.shape):
        if _visible(trees, iy, ix):
            num_visible += 1
    return num_visible

def _visible(trees, iy, ix):
    height = trees[iy, ix]
    size = trees.shape
    if iy == 0 or iy == size[0] - 1 or ix == 0 or ix == size[1] - 1:
        return True
    subset = trees[iy + 1:size[0], ix:ix+1]
    if (np.max(subset) < height):
        return True
    subset = trees[0:iy, ix:ix+1]
    if (np.max(subset) < height):
        return True
    subset = trees[iy:iy+1,ix + 1:size[0]]
    if (np.max(subset) < height):
        return True
    subset = trees[iy:iy+1,0:ix]
    if (np.max(subset) < height):
        return True

    return False

def best_scenic_score(data):
    rows = data.splitlines()
    int_list = [list(map(int, [x for x in row])) for row in rows]
    trees = np.array(int_list)
    best_score = 0
    for iy,ix in np.ndindex(trees.shape):
        if (iy > 0 and iy < trees.shape[0] - 1 and ix > 0 and ix < trees.shape[1]-1):
            score = _score(trees, [iy,ix])
            if (score > best_score):
                best_score = score
    return best_score

def _score(trees, curpos):
    return _trees_in_dir(trees, curpos, [-1, 0]) * _trees_in_dir(trees, curpos, [1,0]) * _trees_in_dir(trees, curpos, [0,-1]) * _trees_in_dir(trees,curpos,[0,1])

def _trees_in_dir(trees, curpos, direction):
    count = 0
    target_height = trees[curpos[0],curpos[1]]
    pos = list(curpos)
    while True:
        pos[0] += direction[0]
        pos[1] += direction[1]
        if pos[0] < 0 or pos[0] == trees.shape[0] or pos[1] < 0 or pos[1] == trees.shape[1]:
            return count
        count += 1
        cur_height = trees[pos[0],pos[1]]
        if cur_height >= target_height:
            return count
        


ex1 = """30373
25512
65332
33549
35390
"""

assert count_visible(ex1) == 21
print('8a: ', count_visible(data))

assert best_scenic_score(ex1) == 8
print('8b: ', best_scenic_score(data))
