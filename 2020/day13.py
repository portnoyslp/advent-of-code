from functools import reduce

from aocd import data


def get_earliest_bus(input_str):
    buses, timestamp = parse_input(input_str)
    min_time = timestamp
    bus_id = None
    for b in buses:
        if b == 'x':
            continue
        bus = int(b)
        next_bus_time = bus - (timestamp % bus)
        if next_bus_time < min_time:
            min_time = next_bus_time
            bus_id = bus
    return bus_id * min_time


def parse_input(input_str):
    timestamp, bus_list = input_str.splitlines()
    buses = bus_list.split(',')
    timestamp = int(timestamp)
    return buses, timestamp


def gold_coin_timestamp(input_str):
    buses, ignored = parse_input(input_str)
    mods = []
    vals = []
    for i, bus in enumerate(buses):
        if bus == 'x': continue
        bus = int(bus)
        mods.append(bus)
        val = (bus - i) % bus
        vals.append(val)
    return chinese_remainder(mods, vals)


def chinese_remainder(mods_list, vals_list):
    sum = 0
    prod = reduce(lambda a, b: a * b, mods_list)
    for n_i, a_i in zip(mods_list, vals_list):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


assert get_earliest_bus('''939
7,13,x,x,59,x,31,19''') == 295
print('13a: ', get_earliest_bus(data))

assert gold_coin_timestamp('1\n17,x,13,19') == 3417
assert gold_coin_timestamp('''939
7,13,x,x,59,x,31,19''') == 1068781
assert gold_coin_timestamp('1\n67,7,59,61') == 754018
assert gold_coin_timestamp('1\n67,x,7,59,61') == 779210
assert gold_coin_timestamp('1\n67,7,x,59,61') == 1261476
assert gold_coin_timestamp('1\n1789,37,47,1889') == 1202161486
print('13b: ', gold_coin_timestamp(data))
