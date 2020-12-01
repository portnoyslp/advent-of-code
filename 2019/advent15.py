from intcode import Intcode
from enum import IntEnum
import numpy as np


class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def reverse(self):
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.WEST:
            return Direction.EAST
        return Direction.WEST

    def vector(self):
        vec = [0, 0]
        if self == Direction.NORTH:
            vec[1] -= 1
        elif self == Direction.SOUTH:
            vec[1] += 1
        elif self == Direction.WEST:
            vec[0] -= 1
        elif self == Direction.EAST:
            vec[0] += 1
        return vec


class Status(IntEnum):
    WALL = 0
    MOVED = 1
    OXYGEN = 2


def adjust_position(position, direction):
    vec = direction.vector()
    return position[0] + vec[0], position[1] + vec[1]


class Droid:
    def __init__(self):
        droid_program = '3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,1002,1036,1,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1001,1034,0,1039,1001,1036,0,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,1002,1035,1,1040,1001,1038,0,1043,1002,1037,1,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,1001,1038,0,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,3,1032,1006,1032,165,1008,1040,5,1032,1006,1032,165,1101,2,0,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,55,1044,1106,0,224,1102,0,1,1044,1105,1,224,1006,1044,247,102,1,1039,1034,102,1,1040,1035,102,1,1041,1036,1002,1043,1,1038,101,0,1042,1037,4,1044,1106,0,0,5,20,51,81,57,10,21,4,5,12,94,86,11,35,82,29,14,52,78,53,41,88,58,48,50,16,2,36,58,7,93,31,1,99,43,9,47,67,54,39,78,89,3,17,63,95,70,84,41,59,32,80,35,7,91,36,80,66,28,78,20,26,68,69,59,14,90,22,31,86,16,67,67,45,77,29,61,44,44,77,52,81,54,66,15,43,95,13,22,79,80,37,90,65,58,11,14,80,82,42,84,47,71,14,94,78,24,71,25,6,11,71,47,86,20,97,37,18,92,57,15,98,44,78,91,44,83,59,4,12,87,3,12,14,86,70,19,31,72,29,12,22,23,73,61,91,40,66,68,66,16,73,59,41,83,8,7,48,61,54,95,2,25,61,13,17,76,85,96,16,79,84,39,96,49,24,67,88,88,88,66,46,52,54,71,47,63,84,4,33,7,63,84,27,6,26,76,70,29,49,93,31,63,64,26,16,40,60,30,60,10,85,85,62,32,4,98,39,20,1,85,98,48,29,24,74,30,92,90,37,49,29,95,12,98,49,57,36,43,96,99,17,18,95,26,80,20,29,50,73,69,51,50,9,46,78,38,72,88,39,3,92,96,50,88,14,98,93,7,62,15,97,15,33,21,96,15,74,76,38,12,63,77,80,29,91,96,23,18,75,52,96,78,94,88,49,65,43,82,58,46,27,62,2,32,81,45,67,83,80,62,54,40,85,66,48,54,72,87,3,7,86,84,2,45,46,82,84,17,36,29,94,12,47,59,89,28,93,40,50,77,83,48,66,18,15,70,13,68,26,86,46,18,63,6,97,21,76,75,80,1,30,67,38,74,8,9,65,90,68,11,66,60,12,4,96,94,60,36,25,78,13,67,70,35,76,53,11,72,40,70,59,9,11,88,27,44,61,11,54,98,69,35,93,93,9,85,2,78,21,99,96,27,81,40,9,99,42,66,77,10,95,7,31,90,44,89,90,24,24,48,75,69,36,5,94,89,17,81,52,92,15,52,76,65,35,22,17,58,40,18,2,77,72,49,73,36,35,62,24,64,12,70,1,11,24,82,20,53,80,97,49,70,6,95,12,62,58,12,49,77,80,24,49,86,97,95,45,71,90,60,38,94,23,37,85,1,77,26,57,81,30,58,67,39,60,10,3,82,21,41,71,38,49,65,19,4,93,57,2,74,12,96,12,22,7,50,87,76,51,33,1,90,66,12,85,79,28,18,66,35,21,89,51,83,14,32,63,12,71,40,63,4,95,7,72,65,20,45,79,16,75,85,58,16,74,17,53,88,64,75,29,21,24,51,85,51,97,44,49,67,59,90,29,7,8,98,22,52,94,65,31,83,64,29,43,95,11,68,88,18,35,80,78,39,96,22,94,10,31,93,9,71,43,64,80,67,17,63,50,49,75,14,76,31,89,21,73,30,3,69,97,60,27,24,22,66,27,68,89,69,12,49,91,48,54,60,5,84,69,18,67,1,63,51,28,23,97,4,62,21,13,45,99,33,69,99,5,95,32,54,45,72,99,65,8,54,1,91,27,50,91,65,13,91,16,90,48,12,58,66,86,15,78,68,50,94,7,71,84,87,38,39,16,27,70,61,5,95,92,85,54,72,8,95,81,78,5,92,77,50,74,86,1,31,69,94,1,37,57,32,3,7,92,82,68,90,42,22,71,25,71,71,91,37,93,52,57,18,57,23,83,39,72,25,58,6,69,46,83,19,82,48,70,28,89,98,62,48,69,81,78,24,82,47,82,40,97,10,93,0,0,21,21,1,10,1,0,0,0,0,0,0'
        self.droid = Intcode(droid_program)
        self.curpos = (0, 0)
        self.walls = {}
        self.visited = {}
        # queue of moves to try
        self.nextMoves = []
        self.oxygen_loc = []

    def mark_wall(self, direction):
        # Marks wall in given direction
        wallpos = adjust_position(self.curpos, direction)
        self.walls[f"{wallpos}"] = 1

    def known_pos(self, direction):
        checkpos = adjust_position(self.curpos, direction)
        if f"{checkpos}" in self.visited.keys():
            return True
        if f"{checkpos}" in self.walls.keys():
            return True
        return False

    def step(self, direction):
        self.droid.input(int(direction))
        output_status = self.droid.execute()
        if output_status is None:
            raise RuntimeError('Unexpected end of program')
        if output_status == Status.WALL:
            # We did not move, but there is a wall
            self.mark_wall(direction)
            return Status.WALL
        # Move
        self.curpos = adjust_position(self.curpos, direction)
        if output_status == Status.OXYGEN:
            self.oxygen_loc = self.curpos
        return output_status

    def render_board(self):
        # figure out size of board
        minpos = [100000, 100000]
        maxpos = [-100000, -100000]
        for coord_str in [*self.walls]:
            coord = list(map(int, coord_str[1:-1].split(',')))
            if coord[0] < minpos[0]:
                minpos[0] = coord[0]
            if coord[0] > maxpos[0]:
                maxpos[0] = coord[0]
            if coord[1] < minpos[1]:
                minpos[1] = coord[1]
            if coord[1] > maxpos[1]:
                maxpos[1] = coord[1]
        # use numpy to set all the wall locations
        board = np.full([maxpos[0] - minpos[0] + 1, maxpos[1] - minpos[0] + 1], ' ')
        for coord_str in [*self.walls]:
            coord = list(map(int, coord_str[1:-1].split(',')))
            board[coord[1] - minpos[1]][coord[0] - minpos[0]] = '#'
        # add start and oxygen
        board[-minpos[1]][-minpos[0]] = 'S'
        board[self.oxygen_loc[1] - minpos[1]][self.oxygen_loc[0] - minpos[0]] = 'O'
        # render
        str_board = '\n'.join([''.join(row) for row in board])
        print(f"{str_board}")

    # recursively search a new node, after walking in the given direction (or just start with this node if
    # direction is None)
    def search_node(self, direction=None):
        if direction is not None:
            step_result = self.step(direction)
            if step_result == Status.WALL:
                # we didn't search the node, and we didn't move, so we can just return
                return
        # Mark current position as visited
        self.visited[f"{self.curpos}"] = 1
        for next_dir in list(Direction):
            # Try each direction (except backtracking)
            if next_dir.reverse() != direction and not self.known_pos(next_dir):
                self.search_node(next_dir)
        # Go back from whence we came, and return
        if direction is not None:
            self.step(direction.reverse())

    def run(self):
        self.search_node()
        # OK, at this point we know the oxygen node location.
        self.render_board()

    def shortest_path_from_point(self, startpos=(0,0)):
        # Djikstra
        pending_nodes = {}
        min_dist = {}
        for key in self.visited.keys():
            min_dist[key] = 10000
            pending_nodes[key] = 1
        min_dist[f"{startpos}"] = 0
        while len(pending_nodes.keys()) > 0:
            # find pending node with shortest min_dist
            best_key = sorted([*pending_nodes], key=lambda x: min_dist[x])[0]
            del pending_nodes[best_key]
            new_dist = min_dist[best_key] + 1
            coord = list(map(int, best_key[1:-1].split(',')))
            for direction in list(Direction):
                checkpos = adjust_position(coord, direction)
                if f"{checkpos}" in pending_nodes.keys():
                    min_dist[f"{checkpos}"] = new_dist
        return min_dist

    def shortest_path_to_oxygen(self):
        min_dist = self.shortest_path_from_point()
        return min_dist[f"{self.oxygen_loc}"]

    def time_to_fill_with_oxygen(self):
        min_dist = self.shortest_path_from_point(self.oxygen_loc)
        return max(min_dist.values())

droid = Droid()
droid.run()
print(f"15a: oxygen_pos: {droid.oxygen_loc}")
print(f"15a: shortest_dist: {droid.shortest_path_to_oxygen()}")
print(f"15b: time_to_fill: {droid.time_to_fill_with_oxygen()}")
