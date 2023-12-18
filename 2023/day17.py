from aocd import data

class Grid:
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]

    def __init__(self, data) -> None:
        self.grid = [ [ int(x) for x in row ] for row in data.splitlines() ]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.start = (0,0)
        self.end = (self.width - 1, self.height - 1)
        self.step_range = [1,3]

    def set_range(self, m, n):
        self.step_range = [m,n]
        return self

    def min_heat_loss(self):
        # calculate best path from start to end, with minimal heat loss
        # dijkstra's algorithm, with nodes consisting of (x,y,dir)
        # dir is the index in self.dirs
        dist = {} # distance to node
        prev = {} # previous node for each in a chain
        visited = set()
        q = []
        start_node = (self.start[0],self.start[1],None)
        dist[start_node] = 0
        q.append(start_node)

        while len(q) > 0:
            node = q.pop(0)
            if node in visited:
                continue

            neighbor_map = self.neighbors(node)
            for neighbor,loss in neighbor_map.items():
                cum_loss = dist[node] + loss
                if neighbor not in dist or cum_loss < dist[neighbor]:
                    dist[neighbor] = cum_loss
                    prev[neighbor] = node
                    q.append(neighbor)
            visited.add(node)
            # resort queue
            q.sort(key=lambda x: dist[x])
        
        end_nodes = [x for x in visited if x[0]==self.end[0] and x[1] == self.end[1]]
        # for node in end_nodes:
        #     self.print_path(node, prev)
        dists = list(map(lambda x: dist[x], end_nodes))
        return min(dists)

    def neighbors(self, node):
        result = {} # map of destination nodes to the heat loss generated to get there.
        x,y,old_dir_idx = node
        for dir_idx, d in enumerate(self.dirs):
            if dir_idx == old_dir_idx:
                continue
            # can't reverse direction:
            if (dir_idx^1) == old_dir_idx:
                continue
            cum_loss = 0
            for step in range(1,self.step_range[1] + 1):
                new_node = (x + step * d[0], y + step * d[1], dir_idx)
                if new_node[0] >= 0 and new_node[1] >= 0 and new_node[0] < self.width and new_node[1] < self.height:
                    cum_loss += self.grid[new_node[1]][new_node[0]]
                    if step in range(self.step_range[0], self.step_range[1] + 1):
                        result[new_node] = cum_loss
        return result

    def print_path(self, node, prev):
        chain = [node]
        while node != (self.start[0],self.start[1],None):
            node = prev[node]
            chain.append(node)
        chain.reverse()
        print (' -> '.join([f'{x}' for x in chain]))

def run(data, part=1):
    grid = Grid(data)
    if part == 2:
        grid.set_range(4,10)
    return grid.min_heat_loss()

ex1='''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''

assert run(ex1) == 102
print('17a: ', run(data))
assert run(ex1, part=2) == 94
print('17b: ', run(data, part=2))