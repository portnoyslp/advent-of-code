from aocd import data
from dataclasses import dataclass
import re
import functools

@dataclass
class Valve:
    id: str
    rate: int
    leads_to: set[str]

valves = {}

def best_pressure(data, part=1):
    global valves
    valves.clear()
    calc_pressure.cache_clear()
    for line in data.splitlines():
        match = re.match('Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$', line)
        valve = Valve(match.group(1), int(match.group(2)), set(match.group(3).split(', ')))
        valves[valve.id] = valve
    
    return calc_pressure(frozenset(), 30 if part == 1 else 26, 'AA', part==2)

@functools.cache
def calc_pressure(open_valves, minutes_left, current_valve_id, is_elephant=False):

    if minutes_left <= 0:
        if is_elephant:
            return calc_pressure(open_valves, 26, 'AA')
        return 0
    
    max_pressure = 0
    current_valve = valves[current_valve_id]
    # Travel to neighboring locations
    for dest in current_valve.leads_to:
        max_pressure = max(max_pressure, calc_pressure(open_valves, minutes_left - 1, dest, is_elephant))

    # Can we open this valve?
    if current_valve_id not in open_valves and current_valve.rate > 0 and minutes_left > 0:
        open_valves = set(open_valves)
        open_valves.add(current_valve_id)
        minutes_left -= 1
        pressure_released = current_valve.rate * minutes_left
        # Travel to neighboring locations
        for dest in current_valve.leads_to:
            max_pressure = max(max_pressure, pressure_released + calc_pressure(frozenset(open_valves), minutes_left - 1, dest, is_elephant))

    return max_pressure


ex1 = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''

assert best_pressure(ex1) == 1651
print('16a: ', best_pressure(data))
assert best_pressure(ex1, part=2) == 1707
print('16b: ', best_pressure(data, part=2))
