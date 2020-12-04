from aocd import data
import networkx


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

    def __connections(self, start_item, have_keys=[]):
        return list(
            filter(lambda item: item != start_item and item not in have_keys and item.islower(), self.items.keys()))

    @staticmethod
    def __is_door(item):
        return item != '' and item.isupper()

    @staticmethod
    def __key_for_door(item):
        return item.lower()

    def build_key_graph(self):
        # The key graph is a directed graph where the nodes are referenced by the item name and the list of keys
        # collected to that point. The edges are annotated with the length required.
        # Start with @
        self.key_graph.add_node('@:')
        pending_nodes = ['@:']
        while len(pending_nodes) > 0:
            origin_node = pending_nodes.pop()
            loc_item, key_list = origin_node.split(':')
            key_list = [key for key in key_list]
            for connection in self.__connections(self.items[loc_item], key_list):
                path = networkx.shortest_path(self.plan_graph, self.items[loc_item], self.items[connection])
                # If we can draw a path to that node with these keys, create a new node and edge.
                is_good_path = True
                for node in path:
                    plan_node = self.plan_graph.nodes[node]
                    item = plan_node['item'] if 'item' in plan_node else '-'
                    if self.__is_door(item) and self.__key_for_door(item) not in key_list:
                        is_good_path = False
                        break
                if is_good_path:
                    new_key_list = [key for key in key_list]
                    new_key_list.append(connection)
                    new_key_list.sort()
                    dest_node = connection + ':' + ''.join(new_key_list)
                    self.key_graph.add_node(dest_node)
                    self.key_graph.add_edge(origin_node, dest_node, weight=len(path) - 1)
                    pending_nodes.append(dest_node)

    def shortest_path_length(self):
        self.build_plan_graph()
        self.build_key_graph()
        # Find shortest path in key graph from @ to any node with all the keys.
        all_keys = list(filter(lambda x: x.islower(), self.items.keys()))
        all_keys.sort()
        dest_nodes = list(filter(lambda node: node.endswith(''.join(all_keys)), self.key_graph.nodes()))
        shortest_path = 100000
        start_node = '@:'
        for dest_node in dest_nodes:
            len = networkx.shortest_path_length(self.key_graph, start_node, dest_node, weight='weight')
            if len < shortest_path:
                shortest_path = len
        return shortest_path


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
