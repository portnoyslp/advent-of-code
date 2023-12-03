from aocd import data
import re

def dist_coords(sx, sy, bx, by):
    return abs(bx - sx) + abs(by - sy)
def dist_sensor(t1, x, y):
    return dist_coords(t1[0], t1[1], x, y)

class SensorArray:
    def __init__(self, data):
        self.known_beacons = set() # (x,y) tuples
        self.sensors = {} # (x,y) -> dist

        for line in data.splitlines():
            match = re.match('Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)', line)
            (sx, sy, bx, by) = [int(d) for d in match.groups()]
            self.known_beacons.add((bx,by))
            self.sensors[(sx, sy)] = dist_coords(sx,sy,bx,by)

    def min_x(self):
        return min([sensor[0] - dist for (sensor,dist) in self.sensors.items()])    
    def max_x(self):
        return max([sensor[0] + dist for (sensor,dist) in self.sensors.items()])    

    def merged_ranges(self, row):
        sensor_ranges = []
        for sensor,d in self.sensors.items():
            (x,y) = sensor
            delta_y = abs(row - y)
            if d > delta_y:
                sensor_ranges.append([x - (d - delta_y), x + (d - delta_y)])
        sensor_ranges.sort(key=lambda x:x[0])
        merged_ranges = [sensor_ranges[0]]
        for range in sensor_ranges[1:]:
            if merged_ranges[-1][0] <= range[0] <= merged_ranges[-1][1]:
                merged_ranges[-1][1] = max(range[1],merged_ranges[-1][1])
            else:
                merged_ranges.append(range)
        return merged_ranges

    def count_deadspots(self, row):
        merged_ranges = self.merged_ranges(row)
        # self.show_sensor((8,7), -2, -2, 22, 25)
        cnt = sum([x[1] - x[0] + 1 for x in merged_ranges])
        # If there are any known beacons on this row that are in a range, remove them.
        beacon_cols = [b[0] for b in self.known_beacons if b[1] == row]
        for col in beacon_cols:
            for range in merged_ranges:
                if range[0] <= col <= range[1]:
                    cnt -= 1
                    break
        return cnt
    
    def find_distress_beacon(self):
        # Find a sensor, and evaluate the vertical range of it. Scan those ranges, 
        # and find a row that has two merged ranges separated by a single empty 
        # square. Above and below should be contiguous.
        checked_rows = set()
        for sensor in self.sensors.keys():
            dist = self.sensors[sensor]
            for ybar in range(sensor[1] - dist -1, sensor[1] + dist + 1):
                if ybar in checked_rows:
                    continue
                checked_rows.add(ybar)
                ranges = self.merged_ranges(ybar)
                if len(ranges) > 1:
                    for i in range(1,len(ranges)):
                        if ranges[i][0] - ranges[i-1][1] == 2:
                            # coord is at (ranges[i][0]-1, ybar)
                            return 4000000 * (ranges[i][0] - 1) + ybar
        return None

    def show_sensor(self, sensor, minx, miny, maxx, maxy):
        dist = self.sensors[sensor]
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                if (x,y) in self.known_beacons:
                    print('B', end='')
                elif (x,y) in self.sensors:
                    print('S', end='')
                elif dist_sensor(sensor,x,y) <= dist:
                    print('#', end='')
                else:
                    print('.', end='')
            print("")


ex1='''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''

assert SensorArray(ex1).count_deadspots(10) == 26
print('15a: ', SensorArray(data).count_deadspots(2000000))
assert SensorArray(ex1).find_distress_beacon() == 56000011
print('15b: ', SensorArray(data).find_distress_beacon())
