from aocd import data
import networkx as nx
import re
from itertools import permutations


class DeliveryGraph:
    def __init__(self):
        self.G = nx.Graph()

    def connect(self, line):
        src, dest, dist = re.match(r'(\w+) to (\w+) = (\d+)', line).groups()
        self.G.add_edge(src, dest, weight=int(dist))

    def connect_all(self, input_str):
        for line in input_str.splitlines():
            self.connect(line)
        return self

    def shortest_route(self):
        min_len = 1000000
        for perm in permutations(self.G.nodes, len(self.G.nodes)):
            cur_len = 0
            for idx, node in enumerate(perm[:-1]):
                cur_len += self.G.get_edge_data(node, perm[idx + 1])['weight']
                if cur_len > min_len:
                    break
            if cur_len < min_len:
                min_len = cur_len
        return min_len

    def longest_route(self):
        max_len = 0
        for perm in permutations(self.G.nodes, len(self.G.nodes)):
            cur_len = 0
            for idx, node in enumerate(perm[:-1]):
                cur_len += self.G.get_edge_data(node, perm[idx + 1])['weight']
            if cur_len > max_len:
                max_len = cur_len
        return max_len


test_input = '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''
assert DeliveryGraph().connect_all(test_input).shortest_route() == 605
print('9a: ', DeliveryGraph().connect_all(data).shortest_route())

assert DeliveryGraph().connect_all(test_input).longest_route() == 982
print('9b: ', DeliveryGraph().connect_all(data).longest_route())
