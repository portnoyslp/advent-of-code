from aocd import data

def count_steps(data):
    rows = data.splitlines()
    start = find_start(rows)
    end = find_end(rows)
    
    return len(shortest_path(rows, start, end)) - 1

def shortest_path(rows, start, end):
    # initial state
    queue = []
    visited = set()

    queue.append([start])
    # loop
    while len(queue) > 0:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:   
            neighbors = unvisited_neighbors(rows, visited, node)
            for new_node in neighbors:
                new_path = list(path)
                new_path.append(new_node)
                if (new_node == end):
                    return new_path
                queue.append(new_path)
            visited.add(node)
    return None

def find_target(rows, target):
    for y,row in enumerate(rows):
        for x,ch in enumerate(row):
            if ch == target:
                return (x,y)
def find_start(rows):
    return find_target(rows, 'S')
def find_end(rows):
    return find_target(rows, 'E')

def unvisited_neighbors(rows, visited, node):
    (x,y) = node
    neighbors = []
    left = (x-1,y)
    if valid_step(node, rows, visited, left):
        neighbors.append(left)
    right = (x+1,y)
    if valid_step(node, rows, visited, right):
        neighbors.append(right)
    up = (x,y-1)
    if valid_step(node, rows, visited, up):
        neighbors.append(up)
    down = (x,y+1)
    if valid_step(node,rows, visited, down):
        neighbors.append(down)
    return neighbors

def valid_step(node,rows,visited,new_node):
    (x,y) = node
    (x1,y1) = new_node
    if x1 < 0 or y1 < 0 or x1 >= len(rows[0]) or y1 >= len(rows):
        return False
    if new_node in visited:
        return False
    cur_val = rows[y][x]
    if cur_val == 'S':
        cur_val = 'a'
    new_val = rows[y1][x1]
    if new_val == 'E':
        new_val = 'z'
    if ord(new_val) - ord(cur_val) > 1:
        return False
    return True


def shortest_steps(data):
    rows = data.splitlines()
    end = find_end(rows)
    
    sources = []
    for y,row in enumerate(rows):
        for x,ch in enumerate(row):
            if ch == 'a' or ch == 'S':
                sources.append((x,y))

    paths = [shortest_path(rows,x,end) for x in sources]
    path_lengths = [1000 if p is None else len(p) - 1 for p in paths]
    return min(path_lengths)


ex1='''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

assert count_steps(ex1) == 31
print('12a: ', count_steps(data))
assert shortest_steps(ex1) == 29
print('12b: ', shortest_steps(data))
