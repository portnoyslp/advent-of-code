from aocd import data
import networkx as nx
import re
from functools import lru_cache

def build_graph(input_str):
    graph = nx.DiGraph()
    for line in input_str.splitlines():
        match = re.match(r'(\w+ \w+) bags contain (no other bags|.+)\.', line)
        if match is None:
            continue
        container = match.group(1)
        if match.group(2) == 'no other bags':
            graph.add_node(container)
            continue
        for bags in re.finditer('(\d+) (\w+ \w+) bags?', match.group(2)):
            graph.add_edge(container, bags.group(2), bag_count=int(bags.group(1)))
    return graph

def count_bag_containers(input_str):
    G = build_graph(input_str)
    pathdict = nx.shortest_path_length(G, target='shiny gold')
    return len(pathdict.keys()) - 1 # ignore empty path at target

@lru_cache(maxsize=None)
def count_bags_contained(graph, node):
    count = 1
    for subbag in graph.neighbors(node):
        count += graph.get_edge_data(node, subbag)['bag_count'] * count_bags_contained(graph, subbag)
    return count

def count_bags_contained_by_gold(input_str):
    G = build_graph(input_str)
    return count_bags_contained(G, 'shiny gold') - 1 # don't count the top bag


test_input1 = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''
assert count_bag_containers(test_input1) == 4

print(f'7a: {count_bag_containers(data)}')

test_input2 = '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.'''
assert count_bags_contained_by_gold(test_input1) == 32
assert count_bags_contained_by_gold(test_input2) == 126
print(f'7b: {count_bags_contained_by_gold(data)}')
