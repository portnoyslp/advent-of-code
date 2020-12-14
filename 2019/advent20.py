from aocd import data
import networkx as nx
import string


class Donut:
    def __init__(self):
        self.maze = []
        self.G = nx.Graph()

    @classmethod
    def create(cls, donut_map):
        donut = cls()
        for line in donut_map.splitlines():
            donut.maze.append(line)
        return donut

    def build_graph(self):
        for y in range(len(self.maze)):
            row = self.maze[y]
            for x in range(len(row)):
                if self.maze[y][x] == '.':
                    self.G.add_node((x, y))
        # Create edges
        for x, y in list(self.G.nodes):
            # Check for other nodes left and down.
            if (x + 1, y) in self.G:
                self.G.add_edge((x, y), (x + 1, y))
            if (x, y + 1) in self.G:
                self.G.add_edge((x, y), (x, y + 1))
            # Check for portals.
            portal_name = None
            if self.maze[y][x - 1] in string.ascii_uppercase:
                portal_name = self.maze[y][x - 2:x]
            if self.maze[y][x + 1] in string.ascii_uppercase:
                portal_name = self.maze[y][x + 1:x + 3]
            if self.maze[y - 1][x] in string.ascii_uppercase:
                portal_name = self.maze[y - 2][x] +  self.maze[y - 1][x]
            if self.maze[y + 1][x] in string.ascii_uppercase:
                portal_name = self.maze[y + 1][x] +  self.maze[y + 2][x]

            if portal_name is not None:
                self.G.add_edge((x, y), portal_name)
        # And now, we turn the non-terminal portals into a direct edge.
        for node in list(self.G.nodes):
            if type(node) is str:
                if len(list(nx.neighbors(self.G, node))) == 2:
                    self.G.add_edge(*nx.neighbors(self.G, node), portal=node)
                    self.G.remove_node(node)

    def count_steps(self):
        self.build_graph()
        path = nx.shortest_path(self.G, source='AA', target='ZZ')
        return len(path) - 3 # don't count the AA/ZZ portal names, or the first open space you start on


test_input = '''         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       '''
assert Donut.create(test_input).count_steps() == 23

test_input2 = '''                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               '''
assert Donut.create(test_input2).count_steps() == 58

print('20a: ', Donut.create(data).count_steps())