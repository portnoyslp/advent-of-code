from aocd import data
from itertools import combinations

class Point3d:
    def __init__(self, *args):
        if len(args) == 1:
            (self.x,self.y,self.z) = map(int,args[0].split(','))
        else:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

    def __repr__(self):
        return f'<{self.x}, {self.y}, {self.z}>'

    def __add__(self, pt):
        return Point3d(self.x + pt.x, self.y + pt.y, self.z + pt.z)

    def __sub__(self, pt):
        return Point3d(self.x - pt.x, self.y - pt.y, self.z - pt.z)

    def __eq__(self, pt):
        return self.x == pt.x and self.y == pt.y and self.z == pt.z
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def dist(self, pt):
        return abs(self.x - pt.x) + abs(self.y - pt.y) + abs(self.z - pt.z)

    def rotate(self, rot):
        # 24 different rotations, caused by swapping axes based on rot_val // 4, 
        # and additional rotation around new z axis based on rot_val % 4.
        if rot // 4 == 0:
            new_point = self
        elif rot // 4 == 1:
            new_point = Point3d(-self.x,self.y,-self.z)
        elif rot // 4 == 2:
            new_point = Point3d(self.z,self.y,-self.x)
        elif rot // 4 == 3:
            new_point = Point3d(-self.z, self.y, self.x)
        elif rot // 4 == 4:
            new_point = Point3d(self.x, self.z, -self.y)
        else:
            new_point = Point3d(self.x, -self.z, self.y)
        
        if rot % 4 == 0:
            return new_point
        elif rot % 4 == 1:
            return Point3d(-new_point.y, new_point.x, new_point.z)
        elif rot % 4 == 2:
            return Point3d(-new_point.x, -new_point.y, new_point.z)
        return Point3d(new_point.y, -new_point.x, new_point.z)

class Scanners:
    def __init__(self, input):
        self.scanners = []
        idx = -1
        for line in input.splitlines():
            if not line:
                continue
            if line.startswith('---'):
                idx += 1
                self.scanners.append(set())
                continue
            self.scanners[idx].add(Point3d(line))
    
    # returns a tuple with the overlap -- left and right index of the scanners, rotation index
    # and offset to give to right_idx, and the overlapping set of transformed beacons. If no 
    # match is found, returns None.
    def find_overlap(self, left_idx, right_idx):
        left_set = self.scanners[left_idx]
        for rot in range(0, 24):
            right_rotated = set(map(lambda pt: pt.rotate(rot), self.scanners[right_idx]))
            # For each point in left_set, try each point in the rotated set and see if we can
            # find a mapping that yields at least 12 matches in the point intersection.
            for lp in left_set:
                for rp in right_rotated:
                    diff = lp - rp
                    right_transformed = set(map(lambda pt: pt + diff, right_rotated))
                    matches = left_set.intersection(right_transformed)
                    if len(matches) >= 12:
                        return (left_idx, right_idx, rot, diff, matches)
        return None

    # Go through the list of scanners, and find overlaps between scanners. As we do so,
    # add them to the list of found, transformed scanners. We also track the list of explored
    # scanner indices so we know that we've done all we can do with one.
    def solve(self):
        found_scanners = set()
        found_scanners.add(0)
        self.locations = set()
        self.locations.add(Point3d(0,0,0))
        scanners_to_search = [0]
        while scanners_to_search:
            left_idx = scanners_to_search.pop()
            for right_idx in range(0, len(self.scanners)):
                if right_idx not in found_scanners:
                    overlap = self.find_overlap(left_idx, right_idx)
                    if overlap == None:
                        continue
                    # we have an overlap, transform the coordinates for the overlapped 
                    # scanner and stuff it into found_scanners.
                    print(f'scanner {right_idx} should be at {overlap[3]}')
                    self.locations.add(overlap[3])
                    transformed_set = set(map(lambda pt: pt.rotate(overlap[2]) + overlap[3], self.scanners[right_idx]))
                    found_scanners.add(overlap[1])
                    # replace the self.scanners array so that we are properly sync'd up in later find_overlap calls.
                    self.scanners[right_idx] = transformed_set
                    scanners_to_search.append(right_idx)
        # OK, if I've done everything right, then found_scanners should have all the transformed scanners.
        assert(len(found_scanners) == len(self.scanners))
        # Return the list of all beacons by merging together all the found scanner sets.
        beacons = set()
        for found_beacons in self.scanners:
            beacons = beacons.union(found_beacons)
        return beacons

    def count_beacons(self):
        return len(self.solve())

    def furthest_scanner_pair(self):
        max_dist = 0
        for (x,y) in combinations(self.locations, 2):
            dist = x.dist(y)
            if dist > max_dist:
                max_dist = dist
        return max_dist

def count_beacons(input):
    return Scanners(input).count_beacons()


test="""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""
test_solution = Scanners(test)
assert(test_solution.count_beacons() == 79)
assert(test_solution.furthest_scanner_pair() == 3621)

solution = Scanners(data)
print('19a: ', solution.count_beacons())
print('19b: ', solution.furthest_scanner_pair())
