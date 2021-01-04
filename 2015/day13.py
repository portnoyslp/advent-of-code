from aocd import data
import re
import networkx as nx
from itertools import permutations


class DeliveryGraph:
    def __init__(self):
        self.G = nx.Graph()

    def connect(self, line):
        p1, posneg, amt, p2 = re.match(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)', line).groups()
        amt = -int(amt) if posneg == 'lose' else int(amt)
        if self.G.has_edge(p1, p2):
            self.G[p1][p2]['weight'] = self.G[p1][p2]['weight'] + amt
        else:
            self.G.add_edge(p1, p2, weight=int(amt))

    def connect_all(self, input_str):
        for line in input_str.splitlines():
            self.connect(line)
        return self

    def max_happiness(self):
        max_happ = 0
        for perm in permutations(self.G.nodes, len(self.G.nodes)):
            cur_happ = 0
            for idx, node in enumerate(perm):
                next_node_idx = ( idx + 1 ) % len(perm)
                cur_happ += self.G[node][perm[next_node_idx]]['weight']
            if cur_happ > max_happ:
                max_happ = cur_happ
        return max_happ


test_input = '''Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.'''
assert DeliveryGraph().connect_all(test_input).max_happiness() == 330
print('13a: ', DeliveryGraph().connect_all(data).max_happiness())

graph = DeliveryGraph().connect_all(data)
for node in list(graph.G.nodes()):
    graph.connect(f'Me would gain 0 happiness units by sitting next to {node}')
print('13b: ', graph.max_happiness())
