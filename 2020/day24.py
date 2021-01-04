from aocd import data
import re
from collections import defaultdict

directions = {'e': (1, 0), 'w': (-1, 0), 'se': (1, -1), 'sw': (0, -1), 'ne': (0, 1), 'nw': (-1, 1)}


class LobbyLayout:
    def __init__(self):
        # In set if black
        self.black_tiles = set()

    def flip_tile(self, tile_str):
        cur_loc = (0, 0)
        for dir in filter(None, re.split('([ns]?[ew])', tile_str)):
            cur_loc = tuple(sum(p) for p in zip(cur_loc, directions[dir]))
        if cur_loc in self.black_tiles:
            self.black_tiles.remove(cur_loc)
        else:
            self.black_tiles.add(cur_loc)

    def flip_tiles(self, input_str):
        self.setup(input_str)
        return len(self.black_tiles)

    def setup(self, input_str):
        for line in input_str.splitlines():
            self.flip_tile(line)
        return self

    @staticmethod
    def neighbors(loc):
        for dir in directions.values():
            yield tuple(sum(p) for p in zip(loc, dir))

    def num_black_neighbors(self, loc):
        count = 0
        for n in self.neighbors(loc):
            if n in self.black_tiles:
                count += 1
        return count

    def day_flip(self):
        # create a set with all the neighbors of black tiles.
        all_tiles = set()
        for tile in self.black_tiles:
            all_tiles.add(tile)
            for n in self.neighbors(tile):
                all_tiles.add(n)
        # calculate new array.
        new_black_tiles = self.black_tiles.copy()
        for tile in all_tiles:
            n = self.num_black_neighbors(tile)
            if tile in self.black_tiles and (n == 0 or n > 2):
                new_black_tiles.remove(tile)
            if tile not in self.black_tiles and n == 2:
                new_black_tiles.add(tile)
        # replace set with new set.
        self.black_tiles = new_black_tiles

    def flip_for_days(self, num):
        self.print_hex_grid()
        for n in range(num):
            self.day_flip()
            self.print_hex_grid()
            print(f"Day {n+1}: {len(self.black_tiles)}")
        return len(self.black_tiles)

    def print_hex_grid(self):
        min_loc = (1000, 1000)
        max_loc = (-1000, -1000)
        for tile in self.black_tiles:
            min_loc = tuple(min(x) for x in zip(tile, min_loc))
            max_loc = tuple(max(x) for x in zip(tile, max_loc))
        array = []
        for y in range(max_loc[1], min_loc[1] - 1, -1):
            line = []
            for x in range(min_loc[0], max_loc[0] + 1):
                line.append('#' if (x,y) in self.black_tiles else '.')
            arr_offset = ' ' * (y - min_loc[1]) * 2
            array.append(arr_offset + ('  '.join(line)) + f" {y}")
        print('\n'.join(array))

test_string = '''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew'''
assert LobbyLayout().flip_tiles(test_string) == 10
print('24a: ', LobbyLayout().flip_tiles(data))

assert LobbyLayout().setup(test_string).flip_for_days(10) == 37
assert LobbyLayout().setup(test_string).flip_for_days(100) == 2208
print('24b: ', LobbyLayout().setup(data).flip_for_days(100))
