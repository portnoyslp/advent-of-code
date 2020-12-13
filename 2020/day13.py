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


assert get_earliest_bus('''939
7,13,x,x,59,x,31,19''') == 295
print('13a: ', get_earliest_bus(data))

assert gold_coin_timestamp('''939
7,13,x,x,59,x,31,19''') == 1068781
assert gold_coin_timestamp('1\n17,x,13,19') == 3417
assert gold_coin_timestamp('1\n67,7,59,61') == 754018
assert gold_coin_timestamp('1\n67,x,7,59,61') == 779210
assert gold_coin_timestamp('1\n67,7,x,59,61') == 1261476
assert gold_coin_timestamp('1\n1789,37,47,1889') == 1202161486
print('13b: ', gold_coin_timestamp(data))
