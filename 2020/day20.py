from aocd import data
import numpy as np
import re
from collections import defaultdict
from itertools import islice


class Tile:
    def __init__(self):
        self.id = 0
        self.data = np.zeros((0, 0), dtype=int)
        self.edges = []

    # Generates all views on the tile data. 0, 1, 2, 3 are the base image rotated 90, 180, 270. 4-7 are the
    # flipped version, also rotated 90, 180, 270. Note that the flip is across the vertical axis.
    def views(self):
        idx, img = 0, self.data
        while idx < 8:
            yield img
            img = np.rot90(img)
            if idx == 3:
                img = np.flip(img, axis=0)
            idx += 1

    def view(self, n):
        return next(islice(self.views(), n, None))

    def set_edges(self):
        for view in self.views():
            self.edges.append(''.join(['.#'[x] for x in view[0]]))

    @classmethod
    def from_input(cls, tile_str):
        tile = cls()
        data = []
        for line in tile_str.splitlines():
            if ':' in line:
                tile.id = int(re.match(r'Tile (\d+):', line).group(1))
            else:
                data.append([int(x == '#') for x in line])
        tile.data = np.array(data, dtype=int)
        tile.set_edges()
        return tile


class TileArrangement:
    def __init__(self):
        self.tiles = {}
        self.corners = []
        self.tile_array = None
        self.matching_edges = defaultdict(list)
        self.matching_tiles = defaultdict(set)
        self.full_image = None

        sea_monster_str = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''
        sm_data = []
        for line in sea_monster_str.splitlines():
            sm_data.append([int(x == '#') for x in line])
        self.sea_monster = np.array(sm_data)
        self.sea_monster_count = (self.sea_monster == 1).sum()

    @classmethod
    def load_tiles(cls, input_str):
        arrangement = cls()
        for tile_str in input_str.split('\n\n'):
            tile = Tile.from_input(tile_str)
            arrangement.tiles[tile.id] = tile
        arrangement.build_matches()
        return arrangement

    def build_matches(self):
        for tile in self.tiles.values():
            for i, edge in enumerate(tile.edges):
                self.matching_edges[edge].append((tile.id, i))
        for tile in self.tiles.values():
            # Look at first four edges to find # matching tiles.
            for edge in tile.edges[:4]:
                for (x, _) in self.matching_edges[edge]:
                    self.matching_tiles[tile.id].add(x)
            self.matching_tiles[tile.id].remove(tile.id)
        # Find all tiles that only have two matches
        self.corners = [x[0] for x in self.matching_tiles.items() if len(x[1]) == 2]

    def build_array(self):
        from math import sqrt
        side = round(sqrt(len(self.tiles)))
        # Tile array is a nxn grid of tuples with (tile id, view number)
        self.tile_array = np.full((side, side), None)
        # First, we choose a corner. We can just choose the first without loss of generality, and orient it
        # based on where we can match things.
        corner_tile = self.corners[0]
        edges = self.tiles[corner_tile].edges
        for idx in range(4):
            if len(self.matching_edges[edges[idx]]) == 1 and len(self.matching_edges[edges[(idx + 3) % 4]]) == 1:
                # This is the upper-left corner. Mark it.
                self.tile_array[0][0] = (corner_tile, idx)
                break
        # Now, we go through the grid, finding the tiles that fit based on the existing tiles
        for xc in range(side):
            for yc in range(side):
                if xc == 0 and yc == 0:
                    continue
                if yc == 0:
                    # Look to the west
                    (west_tile, view) = self.tile_array[yc][xc - 1]
                    # The edge we care about is the view + 1, but keeping the flip.
                    view = (view + 1) if (view & 3) < 3 else view & 4
                    match_edge = self.tiles[west_tile].edges[view]
                    matches = [edge for edge in self.matching_edges[match_edge] if edge[0] != west_tile]
                    (match_tile, match_view) = matches[0]
                    # Now, the matching edge is actually the vertically flipped version of the edge + 3.
                    match_view = 7 - match_view
                    self.tile_array[yc][xc] = (match_tile, match_view)
                else:
                    # Look north for match
                    (north_tile, view) = self.tile_array[yc - 1][xc]
                    # The edge we care about is the view + 2, but keeping the flip.
                    view ^= 2
                    match_edge = self.tiles[north_tile].edges[view]
                    matches = [edge for edge in self.matching_edges[match_edge] if edge[0] != north_tile]
                    (match_tile, match_view) = matches[0]
                    # Now, the matching edge is actually the vertically flipped version
                    match_view = 4 ^ (((6 - match_view) % 4) | (match_view & 4))
                    self.tile_array[yc][xc] = (match_tile, match_view)

    def atile(self, xc, yc):
        return self.gtile(*self.tile_array[yc][xc])

    def gtile(self, tile_id, view_id):
        return self.tiles[tile_id].view(view_id)

    def create_full_image(self):
        self.build_array()

        # Build a temporary thing so I can make sure everything lines up
        blocks = []
        size = np.shape(self.tile_array)[0]
        for yc in range(size):
            block_row = []
            for xc in range(size):
                block_row.append(self.atile(xc, yc))
            blocks.append(block_row)
        temporary_thing = np.block(blocks)

        blocks = []
        size = np.shape(self.tile_array)[0]
        for yc in range(size):
            block_row = []
            for xc in range(size):
                block_row.append(self.atile(xc, yc)[1:-1, 1:-1])
            blocks.append(block_row)
        self.full_image = np.block(blocks)

    def find_monsters(self):
        from scipy.signal import convolve2d
        img = self.full_image
        for idx in range(8):
            monster_hunts = convolve2d(img, np.flip(self.sea_monster), mode='valid')
            monster_count = (monster_hunts == self.sea_monster_count).sum()
            if monster_count > 0:
                return monster_count
            img = np.rot90(img)
            if idx == 3:
                img = np.flip(img, axis=0)
        return 0

    def print_boolean_image(self, arr):
        return (lambda x: '.#'[x])(arr)

def find_corners(input_str):
    arr = TileArrangement.load_tiles(input_str)
    from functools import reduce
    return reduce(lambda x, y: x * y, arr.corners)


def test_input():
    return '''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...'''


assert find_corners(test_input()) == 20899048083289
print('20a: ', find_corners(data))


def find_monsters_and_roughness(input_str):
    arr = TileArrangement.load_tiles(input_str)
    arr.create_full_image()
    num_monsters = arr.find_monsters()
    return np.sum(arr.full_image) - num_monsters * arr.sea_monster_count


assert find_monsters_and_roughness(test_input()) == 273
print('20b: ', find_monsters_and_roughness(data))
