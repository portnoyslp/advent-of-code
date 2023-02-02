from aocd import lines
from collections import defaultdict
import re

def count_cubes(inputlines):
    cubes = defaultdict(bool)
    for line in inputlines:
        (switch, x1, x2, y1, y2, z1, z2) = re.match(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line).groups()
        turn_on = switch == 'on'
        for x in range(max(int(x1),-50), min(int(x2)+1, 51)):
            for y in range(max(int(y1), -50), min(int(y2) + 1, 51)):
                for z in range(max(int(z1),-50), min(int(z2) + 1, 51)):
                        cubes[(x,y,z)] = turn_on
    return sum(cubes.values())

test = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""
assert(count_cubes(test.splitlines()) == 590784)
print('22a: ', count_cubes(lines))    

def range_overlap(r1, r2):
    return (r1[0] <= r2[1]) and (r1[1] >= r2[0])
def range_intersect(r1, r2):
    point1 = min(r1[0], r2[1])
    point2 = max(r2[0], r1[1])
    return (min(point1, point2), max(point1, point2))

class Volume:
    def __init__(self, xr, yr, zr, turned_on):
        self.turned_on = turned_on
        (self.x, self.y, self.z) = (list(xr), list(yr), list(zr))
        # voids are the sub-spaces that are perhaps the opposite value from the main valume.
        self.voids = []
    

    @classmethod
    def parse(cls, line):
        (switch, x1, x2, y1, y2, z1, z2) = re.match(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line).groups()
        return cls(map(int, [x1, x2]), map(int, [y1, y2]), map(int, [z1, z2]), switch == 'on')

    def count_on(self):
        return (self.volume() if self.turned_on else 0) + sum([ v.count_on() for v in self.voids ])

    def volume(self):
        return (self.x[1] - self.x[0]) * (self.y[1] - self.y[0]) * (self.z[1] - self.z[0]) - sum([v.volume() for v in self.voids])

    def intersect(self, vol):
        if range_overlap(self.x, vol.x) and range_overlap(self.y, vol.y) and range_overlap(self.y, vol.y):
            self.voids.append(Volume(range_intersect(self.x, vol.x), range_intersect(self.y, vol.y), range_intersect(self.z, vol.z), vol.turned_on))

volumes = []
for volstr in test.splitlines()[0:-2]:
    new_volume = Volume.parse(volstr)
    for v in volumes:
        v.intersect(new_volume)
    volumes.append(new_volume)
sizes = list([v.count_on() for v in volumes])
assert(sum([v.count_on() for v in volumes]) == 590784)
    
