from aocd import data
import networkx
from functools import lru_cache


class Vault:
    def __init__(self):
        self.vault = []
        self.plan_graph = networkx.Graph()
        self.key_graph = networkx.DiGraph()
        self.items = {}

    @classmethod
    def create_vault(cls, vault_map):
        vault = cls()
        for line in vault_map.splitlines():
            vault.vault.append(line)
        return vault

    def build_plan_graph(self):
        # Nodes are identified by 1000*xc + yc.
        for yc in range(len(self.vault)):
            row = self.vault[yc]
            for xc in range(len(row)):
                if self.vault[yc][xc] == '#':
                    continue
                node = 1000 * xc + yc
                if self.vault[yc][xc] == '.':
                    self.plan_graph.add_node(node)
                else:
                    self.plan_graph.add_node(node, item=self.vault[yc][xc])
                    self.items[self.vault[yc][xc]] = node
        # Create edges
        for n in self.plan_graph.nodes.items():
            node = n[0]
            node2 = node + 1
            if node2 in self.plan_graph:
                self.plan_graph.add_edge(node, node2)
            node2 = node + 1000
            if node2 in self.plan_graph:
                self.plan_graph.add_edge(node, node2)

    def __connections(self, start_item, have_keys=set()):
        return list(
            filter(lambda item: item != start_item and item not in have_keys and item.islower(), self.items.keys()))

    @staticmethod
    def __is_door(item):
        return item != '' and item.isupper()

    @staticmethod
    def __is_key(item):
        return item != '' and item.islower()

    @staticmethod
    def __key_for_door(item):
        return item.lower()

    def __all_keys(self):
        return list(filter(lambda x: x.islower(), self.items.keys()))

    def dijkstra_over_graph(self):
        # Using Dijkstra, go over a simplified version of the graph. Nodes are referenced by the key at the location,
        # and the sorted set of keys that would be collected at that point.
        visited_nodes = set()
        node_distances = {}
        current_node = '@:'  # start location, with no keys
        node_distances[current_node] = 0
        all_keys_set = set(self.__all_keys())
        while True:
            # Generate all unvisited connection nodes.
            loc_item, key_list_str = current_node.split(':')
            key_set = set(key_list_str)
            for connection in self.__connections(self.items[loc_item], key_set):
                # Would we have already visited this node?
                new_set = set(key_set)
                new_set.add(connection)
                new_node = connection + ':' + ''.join(sorted(new_set))
                if new_node in visited_nodes:
                    continue
                path = self.get_plan_path(connection, loc_item)
                # Check for doors or other keys in the way
                is_good_path = True
                for node in path[1:-1]:
                    plan_node = self.plan_graph.nodes[node]
                    item = plan_node['item'] if 'item' in plan_node else '-'
                    if self.__is_door(item) and self.__key_for_door(item) not in key_set:
                        is_good_path = False
                        break
                    if self.__is_key(item) and item not in key_set:
                        # This is considered a non-good path
                        is_good_path = False
                        break
                if is_good_path:
                    if new_node in node_distances:
                        node_distances[new_node] = min(node_distances[new_node],
                                                       node_distances[current_node] + len(path) - 1)
                    else:
                        node_distances[new_node] = node_distances[current_node] + len(path) - 1
            if key_set == all_keys_set:
                # We're done, we've fully visited a node where we have all the keys.
                return node_distances[current_node]
            visited_nodes.add(current_node)
            min_distance = 9999999999
            # Figure out the new current node and continue the loop
            for node, dist in node_distances.items():
                if node not in visited_nodes and dist < min_distance:
                    min_distance = dist
                    current_node = node

    @lru_cache(maxsize=512)
    def get_plan_path(self, connection, loc_item):
        if connection < loc_item:
            return self.get_plan_path(loc_item, connection)
        return networkx.shortest_path(self.plan_graph, self.items[loc_item], self.items[connection])

    def shortest_path_length(self):
        self.build_plan_graph()
        return self.dijkstra_over_graph()


# Plan:
# Load vault plan
# Identify locations of all people, keys, doors.
# Build graph from plan and calculate shortest path between (me, keys)
#   Annotate graph edges with any doors required
# Use first graph to create a search graph
#   New graph has nodes named with loc+keys possessed at node (generate on the fly)
#   Edges annotated with path from node to node.
#   Only add new node if there is an existing node n:[keys] such that n1:[keys + n1] can be reached with
#   the keys in the keys list.
# Calculate paths from @:[no keys] to [some node]:[all keys]
#   Return shortest path length.


def find_length(input_str):
    vault = Vault.create_vault(input_str)
    return vault.shortest_path_length()


def check(input_str, expected_val):
    assert find_length(input_str) == expected_val


check('''#########
#b.A.@.a#
#########
''', 8)
check('''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
''', 86)
check('''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
''', 132)
check('''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
''', 136)
check('''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
''', 81)

print(f'18a: {find_length(data)}')