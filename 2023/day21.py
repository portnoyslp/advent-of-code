from aocd import data

def neighbors(coords):
    x,y = coords
    return [(x - 1, y), (x+1,y), (x,y+1), (x,y-1)]

def shortest_steps(grid, start):
    dist = {}
    queue = []
    for v in grid:
        dist[v] = 100000000000
        queue.append(v)
    dist[start] = 0

    while len(queue) > 0:
        # find min dist u in queue
        u = queue[0]
        u_dist = dist[u]
        for i in queue[1:]:
            if dist[i] < dist[u]:
                u = i
                u_dist = dist[u]
        queue.remove(u)

        for v in neighbors(u):
            if v not in grid or v not in queue:
                continue
            alt = u_dist + 1
            if alt < dist[v]:
                dist[v] = alt
    
    return dist

def run(data, steps):
    grid = set()
    for y,line in enumerate(data.splitlines()):
        for x,ch in enumerate(line):
            if ch == '.' or ch == 'S':
                grid.add( (x, y) )
            if ch == 'S':
                start = (x,y)
    dist_dict = shortest_steps(grid, start)
    # Return the number of entries which have a value <= steps, and the same even/odd parity
    matches = [x for x,d in dist_dict.items() if d <= steps and d%2 == steps%2]
    return len(matches)    

ex1='''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''

assert run(ex1, 6) == 16
print('21a: ', run(data, 64))