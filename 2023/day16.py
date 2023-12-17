from aocd import data

def move(cell, dir):
    return ( cell[0] + dir[0], cell[1] + dir[1] )

class Grid:
    def __init__(self, data):
        self.grid = data.splitlines()
        self.lit = set()
        self.visited = set()

    def illuminate(self, cell, dir):
        self.illuminate_iter(cell, dir)

    def illuminate_iter(self, cell, dir):
        while True:
            # are we off the grid?
            if cell[0] < 0 or cell[1] < 0 or cell[0] >= len(self.grid[0]) or cell[1] >= len(self.grid):
                return
        
            if (cell,dir) in self.visited:
                return
            self.visited.add( (cell,dir) )

            # print(f'Lighting up {cell}')
            self.lit.add(cell)
            ch = self.pos(cell)
            if ch == '.':
                cell = move(cell,dir)
                continue
            if ch == '\\':
                dir = ( dir[1], dir[0] )
                cell = move(cell, dir)
                continue
            if ch == '/':
                dir = ( -dir[1], -dir[0] )
                cell = move(cell, dir)
                continue
            if ch == '-':
                if dir[1] == 0:
                    cell = move(cell, dir)
                    continue
                else:
                    self.illuminate(move(cell, (1,0)), (1,0))
                    dir = (-1,0)
                    cell = move(cell, dir)
                    continue
            if ch == '|':
                if dir[0] == 0:
                    cell = move(cell, dir)
                    continue
                else:
                    self.illuminate(move(cell, (0,1)), (0,1))
                    dir = (0,-1)
                    cell = move(cell, dir)
                    continue
            print(f'Unknown character {ch} @ ({cell})')
    
    def pos(self, tup):
        x,y=tup
        return self.grid[y][x]

    def clear_lit(self):
        self.lit = set()
        self.visited = set()

    def count_lit(self):
        return len(self.lit)
    
    def size(self):
        return ( len(self.grid[0]), len(self.grid))
    
    def __str__(self):
        return '\n'.join(self.grid)

    def __repr__(self):
        return f'Grid with {len(self.lit)} lit elements'

def run_illuminate(grid, cell, dir):
    grid.clear_lit()
    grid.illuminate(cell, dir)
    # print(f'cell {cell} dir {dir} -> {grid.count_lit()}')

def run(data, part=1):
    grid = Grid(data)
    if part == 1:
        grid.illuminate((0,0),(1,0))
        # print(grid)
        return grid.count_lit()
    # illuminate from sides
    max = 0
    size = grid.size()
    for y in range(size[1]):
        run_illuminate(grid, (0, y), (1,0))
        if grid.count_lit() > max:
            max = grid.count_lit()
        run_illuminate(grid, (size[0] - 1, y), (-1,0))
        if grid.count_lit() > max:
            max = grid.count_lit()
    
    for x in range(size[0]):
        run_illuminate(grid, (x,0), (0,1))
        if grid.count_lit() > max:
            max = grid.count_lit()
        run_illuminate(grid, (x, size[1] - 1), (0,-1))
        if grid.count_lit() > max:
            max = grid.count_lit()
    return max


ex1='''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
'''

assert run(ex1) == 46
print('16a: ', run(data))
assert run(ex1, part=2) == 51
print('16b: ', run(data, part=2))