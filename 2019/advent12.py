import numpy as np
import re
import math


def parse_moons(test_spec):
    parse_output = []
    for line in test_spec.splitlines():
        pattern = r'x=(-?\d+), y=(-?\d+), z=(-?\d+)'
        match = re.search(pattern, line)
        if match is not None:
            parse_output.append([int(i) for i in match.groups()])
    positions = np.array(parse_output)
    velocity = np.zeros(np.shape(positions))
    return [positions, velocity]


def cmp(a, b):
    """Returns 1 if a > b, 0 if equal, and -1 if a < b"""
    if a == b: return 0
    if a > b: return 1
    return -1


def update_positions_and_velocity(positions, velocity):
    dv = np.zeros(np.shape(velocity))
    # Update dv array with sum of comparisons. This is probably best done with a matrix
    # multiply, but I'm still trying to figure out numpy.
    num_moons = np.shape(positions)[0]
    num_axes = np.shape(positions)[1]
    for moon1 in range(num_moons):
        for moon2 in range(num_moons):
            for axis in range(num_axes):
                dv[moon1][axis] += cmp(positions[moon2][axis], positions[moon1][axis])
    velocity = velocity + dv
    return [positions + velocity, velocity]


def system_energy(positions, velocity):
    pot_energies = np.sum(np.abs(positions), axis=1)
    kin_energies = np.sum(np.abs(velocity), axis=1)
    total_energies = pot_energies * kin_energies
    return np.sum(total_energies)


test = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
test_pos_and_vel = parse_moons(test)
print(f"0 steps --> {test_pos_and_vel}")
for i in range(10):
    test_pos_and_vel = update_positions_and_velocity(*test_pos_and_vel)
print(f"10 steps --> {test_pos_and_vel}")
print(f"          --> {system_energy(*test_pos_and_vel)}")

test = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""
test_pos_and_vel = parse_moons(test)
for i in range(100):
    test_pos_and_vel = update_positions_and_velocity(*test_pos_and_vel)
print(f"10 steps --> {test_pos_and_vel}")
print(f"          --> {system_energy(*test_pos_and_vel)}")

real_input = """
<x=-16, y=-1, z=-12>
<x=0, y=-4, z=-17>
<x=-11, y=11, z=0>
<x=2, y=2, z=-6>
"""
pos_and_vel = parse_moons(real_input)
for i in range(1000):
    pos_and_vel = update_positions_and_velocity(*pos_and_vel)
print(f"12a: 1000 steps --> {system_energy(*pos_and_vel)}")

# 12b: After parsing, break the velocities and positions independently by axis so that we can find loops quicker
test = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
test_pos_and_vel = parse_moons(test)


def find_loop(positions_and_velocities):
    coord_str = f"{positions_and_velocities}"
    seen_positions = {}
    counter = 0
    seen_positions[coord_str] = counter
    while True:
        positions_and_velocities = update_positions_and_velocity(*positions_and_velocities)
        counter += 1
        coord_str = f"{positions_and_velocities}"
        if coord_str in seen_positions.keys():
            break
        seen_positions[coord_str] = counter
    return seen_positions[coord_str], counter


def lcm(a, b):
    g = math.gcd(a, b)
    return math.floor((a * b) / g)


def find_repeats(positions_and_velocities):
    x_coords = [positions_and_velocities[0][:, [0]], positions_and_velocities[1][:, [0]]]
    x_output = find_loop(x_coords)
    y_coords = [positions_and_velocities[0][:, [1]], positions_and_velocities[1][:, [1]]]
    y_output = find_loop(y_coords)
    z_coords = [positions_and_velocities[0][:, [2]], positions_and_velocities[1][:, [2]]]
    z_output = find_loop(z_coords)

    if x_output[0] == y_output[0] and y_output[0] == z_output[0]:
        # Same start point, so find lcm of repeat values
        x_repeat = x_output[1] - x_output[0]
        y_repeat = y_output[1] - y_output[0]
        z_repeat = z_output[1] - z_output[0]
        lcm_xy = lcm(x_repeat, y_repeat)
        lcm_xyz = lcm(lcm_xy, z_repeat)
        return lcm_xyz
    return None


assert find_repeats(test_pos_and_vel) == 2772

final_answer = find_repeats(pos_and_vel)
print(f"12b --> {final_answer}")
