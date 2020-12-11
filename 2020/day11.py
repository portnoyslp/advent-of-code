from aocd import data
from scipy.signal import convolve2d
import numpy as np


class Seating:
    def __init__(self):
        self.neighbor_filter = np.ones((3, 3), dtype=int)
        self.neighbor_filter[1][1] = 0
        self.seat_mask = None

    def parse_input(self, input_str):
        seating = []
        for line in input_str.splitlines():
            if line != '':
                seating.append([c for c in line])
        # Turn into two np arrays; a seating mask and an occupation array
        seat_mask_map = {'L': True, '.': False}
        self.seat_mask = np.vectorize(seat_mask_map.get)(seating)
        return np.zeros(self.seat_mask.shape, dtype=bool)

    def steady_state(self, occupied, new_occ_fn=None):
        if new_occ_fn is None:
            new_occ_fn = self.get_new_occupied
        while True:
            new_occupied = new_occ_fn(occupied)
            if np.array_equal(new_occupied, occupied):
                return occupied
            occupied = new_occupied

    def get_new_occupied(self, occupied):
        # convolve with neighbor count
        num_neighbors = convolve2d(occupied, self.neighbor_filter, mode='same')
        new_occupied = ((num_neighbors == 0) | (occupied & (num_neighbors < 4))) & self.seat_mask
        return new_occupied

    def new_occ_11b(self, occupied):
        # Determine neighbors by looking in every direction for an empty seat.
        num_neighbors = np.zeros(occupied.shape, dtype=int)
        for xc in range(occupied.shape[0]):
            for yc in range(occupied.shape[1]):
                if self.seat_mask[xc][yc]:
                    for dir in [(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)]:
                        occ = self.seat_in_dir_occupied((xc,yc), dir, occupied)
                        if (occ):
                            num_neighbors[xc][yc] += 1
        new_occupied = ((num_neighbors == 0) | (occupied & (num_neighbors < 5))) & self.seat_mask
        return new_occupied

    def seat_in_dir_occupied(self, origin, dir, occupied):
        cur_seat = origin
        while True:
            cur_seat = (cur_seat[0] + dir[0], cur_seat[1] + dir[1])
            if cur_seat[0] not in range(self.seat_mask.shape[0]) or cur_seat[1] not in range(self.seat_mask.shape[1]):
                return False
            if self.seat_mask[cur_seat[0]][cur_seat[1]]:
                return occupied[cur_seat[0]][cur_seat[1]]

    @classmethod
    def steady_state_num_occupied(cls, input_str):
        seating = cls()
        occupied = seating.parse_input(input_str)
        occupied = seating.steady_state(occupied)
        return (occupied == 1).sum()

    @classmethod
    def steady_state_num_occupied_11b(cls, input_str):
        seating = cls()
        occupied = seating.parse_input(input_str)
        occupied = seating.steady_state(occupied, seating.new_occ_11b)
        return (occupied == 1).sum()


test_input = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''
assert Seating.steady_state_num_occupied(test_input) == 37
print('11a: ', Seating.steady_state_num_occupied(data))

assert Seating.steady_state_num_occupied_11b(test_input) == 26
print('11b: ', Seating.steady_state_num_occupied_11b(data))
