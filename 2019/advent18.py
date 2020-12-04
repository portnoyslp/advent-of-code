from aocd import data
import networkx


class Vault:
    def __init__(self):
        self.vault = []
        self.plan_graph = networkx.Graph()
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

    def shortest_path_length(self):
        self.build_plan_graph()
        return 0
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
