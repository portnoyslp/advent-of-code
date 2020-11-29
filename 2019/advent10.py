import math
from collections import defaultdict

def asteroid_coords(map_str):
    coords = []
    lines = map_str.splitlines()
    y = 0
    for line in lines:
        if line == '':
            continue
        start = 0
        while line.find("#", start) != -1:
            coords.append([line.find("#", start), y])
            start = line.find("#", start) + 1
        y += 1
    return coords


def dir_str(coord1, coord2):
    deltax = coord1[0] - coord2[0]
    deltay = coord1[1] - coord2[1]
    if deltax == 0 and deltay == 0:
        return "identity"
    # Use GCD to simplify
    gcd = math.gcd(deltax, deltay)
    deltax = deltax / gcd
    deltay = deltay / gcd
    return f"{deltax},{deltay}"


def coords_for_station(map_str):
    coords = asteroid_coords(map_str)
    best_output = [-1, -1, 0]
    for poss_station in coords:
        dir_dict = {}
        for asteroid in coords:
            dir = dir_str(poss_station, asteroid)
            if dir in dir_dict:
                dir_dict[dir] += 1
            else:
                dir_dict[dir] = 1
        num_seen = len(dir_dict.keys()) - 1
        if num_seen > best_output[2]:
            best_output = [poss_station[0], poss_station[1], num_seen]
    return best_output


small_test_input = """
.#..#
.....
#####
....#
...##
"""
assert coords_for_station(small_test_input) == [3, 4, 8]
test_input = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
assert coords_for_station(test_input) == [5, 8, 33]
test_input = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
assert coords_for_station(test_input) == [1, 2, 35]
test_input = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
assert coords_for_station(test_input) == [6, 3, 41]
big_test_input = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
assert coords_for_station(big_test_input) == [11, 13, 210]

star_input = """
.............#..#.#......##........#..#
.#...##....#........##.#......#......#.
..#.#.#...#...#...##.#...#.............
.....##.................#.....##..#.#.#
......##...#.##......#..#.......#......
......#.....#....#.#..#..##....#.......
...................##.#..#.....#.....#.
#.....#.##.....#...##....#####....#.#..
..#.#..........#..##.......#.#...#....#
...#.#..#...#......#..........###.#....
##..##...#.#.......##....#.#..#...##...
..........#.#....#.#.#......#.....#....
....#.........#..#..##..#.##........#..
........#......###..............#.#....
...##.#...#.#.#......#........#........
......##.#.....#.#.....#..#.....#.#....
..#....#.###..#...##.#..##............#
...##..#...#.##.#.#....#.#.....#...#..#
......#............#.##..#..#....##....
.#.#.......#..#...###...........#.#.##.
........##........#.#...#.#......##....
.#.#........#......#..........#....#...
...............#...#........##..#.#....
.#......#....#.......#..#......#.......
.....#...#.#...#...#..###......#.##....
.#...#..##................##.#.........
..###...#.......#.##.#....#....#....#.#
...#..#.......###.............##.#.....
#..##....###.......##........#..#...#.#
.#......#...#...#.##......#..#.........
#...#.....#......#..##.............#...
...###.........###.###.#.....###.#.#...
#......#......#.#..#....#..#.....##.#..
.##....#.....#...#.##..#.#..##.......#.
..#........#.......##.##....#......#...
##............#....#.#.....#...........
........###.............##...#........#
#.........#.....#..##.#.#.#..#....#....
..............##.#.#.#...........#.....
"""
output = coords_for_station(big_test_input)
print(f"10a -- coords and count is {output}")

# Part 10b
def asteroid_destruction_order(input):
    station_loc = coords_for_station(input)
    # filter out the base coord
    asteroid_locs = filter(lambda c: c[0] != station_loc[0] or c[1] != station_loc[1], asteroid_coords(input))
    # translate to base station loc and convert to polar coords with 0-360 angle
    asteroid_locs = map(lambda c: [c[0] - station_loc[0], c[1] - station_loc[1], c], asteroid_locs)
    asteroid_locs = list(asteroid_locs)
    asteroid_locs = map(lambda c: [math.hypot(c[0], c[1]), (math.atan2(c[0], -c[1]) * 180 / math.pi) % 360, c[2]], asteroid_locs)
    asteroid_locs = list(asteroid_locs)
    # create a reverse map so that we can go back to what we need
    reverse_map = {}
    for loc in asteroid_locs:
        reverse_map[f'{loc[0],loc[1]}'] = loc[2]
    # put into a multimap
    asteroids_by_dir = defaultdict(list)
    for loc in asteroid_locs:
        asteroids_by_dir[loc[1]].append(loc[0])
    # sort all entries in dir by
    for distlist in asteroids_by_dir.values():
        distlist.sort()
    # create reorderd list using dictionary
    reordered_coords = []
    # go through asteroids and put in order
    while len(asteroids_by_dir.keys()) > 0:
        for dir in sorted(asteroids_by_dir.keys()):
            dist = asteroids_by_dir[dir]
            reordered_coords.append([dist[0], dir])
            del dist[0]
            if len(dist) == 0:
                del asteroids_by_dir[dir]
    return list(map(lambda c: reverse_map[f"{c[0],c[1]}"], reordered_coords))


test_coords = asteroid_destruction_order(small_test_input)
assert test_coords[0] == [3,2]

test_coords = asteroid_destruction_order(big_test_input)
assert test_coords[0] == [11,12]
assert test_coords[1] == [12, 1]
assert test_coords[2] == [12, 2]
assert test_coords[9] == [12,8]
assert test_coords[49] == [16,9]
assert test_coords[99] == [10,16]

destruction_coords = asteroid_destruction_order(star_input)
winning_bet = destruction_coords[199]
print(f"10b: -> {winning_bet}")