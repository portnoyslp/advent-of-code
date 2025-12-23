from aocd import data

def count_neighbors(grid, r, c):
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
            count += 1
    return count

def find_rolls(grid):
    rolls = []
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                n = count_neighbors(grid, r, c)
                if n < 4:
                    rolls.append((r, c))
    return rolls

def run(data, part=1):
    num_rolls = 0
    grid = data.splitlines()
    rows = len(grid)
    cols = len(grid[0])
    if part == 1:
        rolls = find_rolls(grid)
        return len(rolls)
    
    while True:
        rolls = find_rolls(grid)
        if not rolls:
            break
        num_rolls += len(rolls)
        for r, c in rolls:
            grid[r] = grid[r][:c] + '.' + grid[r][c+1:]
    return num_rolls

ex1='''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''

assert run(ex1) == 13
print('4a: ', run(data))
assert run(ex1, 2) == 43
print('4b: ', run(data, 2))