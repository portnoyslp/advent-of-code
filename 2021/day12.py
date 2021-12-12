from aocd import lines
from collections import defaultdict

class Graph:
    def __init__(self, lines):
        self.graph = defaultdict(list)
        for line in lines:
            (first, second) = line.split('-')
            self.graph[first].append(second)
            self.graph[second].append(first)
        self.V = self.graph.keys()
    
    def count_paths(self, start_node, end_node, part2 = False):
        self.pathCount = 0
        self.allPaths = set()
        visited = defaultdict(int)
        path = []
        self.count_all_paths_util(start_node, end_node, visited, path, part2)
        return self.pathCount
    
    def count_all_paths_util(self, src, dst, visited, path, part2):
        visited[src] += 1
        path.append(src)

        if dst == src:
            pathstr = '-'.join(path)
            if pathstr not in self.allPaths:
                self.pathCount += 1
                self.allPaths.add(pathstr)
        else:
            for n in self.graph[src]:
                if not_already_visited(n, visited, part2):
                    self.count_all_paths_util(n, dst, visited, path, part2)

        path.pop()
        visited[src] -= 1

def not_already_visited(node, visited, part2):
    if node == 'start':
        return False # already visited
    if not part2:
        return node.isupper() or visited[node] < 1
    # how many twice-visited lowercase nodes are there?
    num_doubles = len([entry for entry in visited.items() if entry[1] > 1 and entry[0][0].islower() ])
    return node.isupper() or num_doubles == 0 or visited[node] < 1
    
def count_paths(lines, part2 = False):
    graph = Graph(lines)
    return graph.count_paths('start', 'end', part2)


test1 = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''
test2 = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''

test3 = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
'''

assert(count_paths(test1.splitlines()) == 10)
assert(count_paths(test2.splitlines()) == 19)
assert(count_paths(test3.splitlines()) == 226)
print('12a: ', count_paths(lines))


assert(count_paths(test1.splitlines(), True) == 36)
assert(count_paths(test3.splitlines(), True) == 3509)
print('12b: ', count_paths(lines, True))
