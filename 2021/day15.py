from aocd import lines
import numpy as np
from heapq import heappush,heappop

def short_path_risk(input_lines, expand_array=False):
    G = Graph(input_lines, expand_array)
    path = G.dijsktra(G.start_node(), G.end_node())
    return sum([x[2] for x in path[1:]])

class Graph:
    def __init__(self, input_lines, expanded_array):
        self.array = np.stack([np.fromiter(map(int,line), int) for line in input_lines])
        self.expand_array = expanded_array
    
    def start_node(self):
        return self.node(0,0)

    def shape(self):
        return tuple(map(lambda x: x * 5, np.shape(self.array)))  if self.expand_array else np.shape(self.array)

    def end_node(self):
        far_node = self.shape()
        return self.node(far_node[0] - 1, far_node[1] - 1)

    def node(self,x,y):
        if self.expand_array:
            orig_array_size = np.shape(self.array)
            orig_weight = self.array[x % orig_array_size[0], y % orig_array_size[1]]
            weight = orig_weight + x // orig_array_size[0] + y // orig_array_size[1]
            return (x,y, ((weight - 1) % 9 )+ 1)
        return (x,y,self.array[x,y])

    # nodes are (x,y,val) tuples
    def neighbors(self, cur_node):
        (x,y,_) = cur_node
        ret = []
        if x > 0:
            ret.append(self.node(x-1,y))
        if x < self.shape()[0] - 1:
            ret.append(self.node(x+1,y))
        if y > 0:
            ret.append(self.node(x,y-1))
        if y < self.shape()[1] - 1:
            ret.append(self.node(x,y+1))
        return ret

    def dijsktra(self, initial, end):
        # nodes are (x,y,val) tuples in the array.
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        next_destination_queue = []
        
        while current_node != end:
            visited.add(current_node)
            destinations = self.neighbors(current_node)
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = next_node[2] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                    heappush(next_destination_queue, [weight, next_node])
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
                        heappush(next_destination_queue, [weight, next_node])
            
            while True:
                [weight, current_node] = heappop(next_destination_queue)
                # check if weight matches what we now expect as the shortest path for the node, otherwise move on
                if weight == shortest_paths[current_node][1]:
                    break
            
            # next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            # if not next_destinations:
            #     return "Route Not Possible"
            # # next node is the destination with the lowest weight
            # current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        
        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path




test="""1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

assert(short_path_risk(test.splitlines()) == 40)
print('15a: ', short_path_risk(lines))

assert(short_path_risk(test.splitlines(), True) == 315)
print('starting big search...')
print('15b: ', short_path_risk(lines, True))