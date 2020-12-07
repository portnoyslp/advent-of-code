from aocd import data
import networkx
from functools import lru_cache
import re

class Vault:
    def __init__(self):
        self.vault = []
        self.plan_graph = networkx.Graph()
        self.items = {}
        self.visited_nodes = set()

    @classmethod
    def create_vault(cls, vault_map):
        vault = cls()
        for line in vault_map.splitlines():
            vault.vault.append(line)
        return vault

    def split_start_in_four(self):
        (x, y) = self.find_start_coord()
        self.vault[y - 1] = self.vault[y - 1][:x - 1] + '1#2' + self.vault[y - 1][x+2:]
        self.vault[y] = self.vault[y][:x - 1] + '###' + self.vault[y][x+2:]
        self.vault[y + 1] = self.vault[y + 1][:x - 1] + '3#4' + self.vault[y + 1][x+2:]

    def find_start_coord(self):
        for yc in range(len(self.vault)):
            for xc in range(len(self.vault[yc])):
                if self.vault[yc][xc] == '@':
                    return xc, yc

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

    def __unfound_keys(self, have_keys=set()):
        return list(
            filter(lambda item: item not in have_keys and self.__is_key(item), self.items.keys()))

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
        node_distances = {}
        current_node = '1234:'  # start locations, with no keys
        node_distances[current_node] = 0
        all_keys_set = set(self.__all_keys())
        while True:
            # Generate all unvisited connection nodes.
            new_nodes = self.__fetch_connections(current_node)

            for new_node, path_len in new_nodes:
                if new_node in node_distances:
                    node_distances[new_node] = min(node_distances[new_node],
                                                node_distances[current_node] + path_len - 1)
                else:
                    node_distances[new_node] = node_distances[current_node] + path_len - 1
            loc_items, key_list_str = current_node.split(':')
            key_set = set(key_list_str)
            if key_set == all_keys_set:
                # We're done, we've fully visited a node where we have all the keys.
                return node_distances[current_node]
            self.visited_nodes.add(current_node)
            min_distance = 9999999999
            # Figure out the new current node and continue the loop
            for node, dist in node_distances.items():
                if node not in self.visited_nodes and dist < min_distance:
                    min_distance = dist
                    current_node = node

    def __fetch_connections(self, current_node):
        loc_items, key_list_str = current_node.split(':')
        key_set = set(key_list_str)
        new_nodes = []
        for dest_key in self.__unfound_keys(key_set):
            new_set = set(key_set)
            new_set.add(dest_key)
            for loc_item in loc_items:
                # One of these should have a path
                path = self.get_plan_path(dest_key, loc_item)
                if path is not None:
                    break
            # Replace loc_item with the new one
            new_loc = [dest_key if item == loc_item else item for item in loc_items]
            new_node = ''.join(new_loc) + ':' + ''.join(sorted(new_set))
            if new_node in self.visited_nodes:
                continue
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
                new_nodes.append( (new_node, len(path)))
        return new_nodes

    @lru_cache(maxsize=512)
    def get_plan_path(self, connection, loc_item):
        if connection < loc_item:
            return self.get_plan_path(loc_item, connection)
        if networkx.has_path(self.plan_graph, self.items[loc_item], self.items[connection]):
            return networkx.shortest_path(self.plan_graph, self.items[loc_item], self.items[connection])
        return None

    def shortest_path_length(self):
        self.build_plan_graph()
        return self.dijkstra_over_graph()


def find_length(input_str):
    vault = Vault.create_vault(input_str)
    vault.split_start_in_four()
    return vault.shortest_path_length()


def check(input_str, expected_val):
    assert find_length(input_str) == expected_val


assert find_length('''#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######''') == 8

assert find_length('''###############
#d.ABC.#.....a#
######...######
######.@.######
######...######
#b.....#.....c#
###############''') == 24

assert find_length('''#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############
''') == 32
print(f'18b: {find_length(data)}')
