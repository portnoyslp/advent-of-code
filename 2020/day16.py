from aocd import data
import re
from functools import reduce

class TicketScanner:
    def __init__(self):
        self.fields = {}
        self.my_ticket = ()
        self.nearby_tickets = []
        self.valid_ranges = []
        self.assigned_fields = []

    @classmethod
    def scan_for_errors(cls, input_str):
        from itertools import chain
        scanner = TicketScanner()
        scanner.setup(input_str)
        invalid_sum = 0
        for num in chain.from_iterable(scanner.nearby_tickets):
            if not scanner.valid_num(num):
                invalid_sum += num
        return invalid_sum

    @classmethod
    def parse_my_ticket(cls, input_str):
        from itertools import chain
        scanner = TicketScanner()
        scanner.setup(input_str)
        scanner.discard_invalid_tickets()
        scanner.assign_fields()
        ticket = {}
        for i in range(len(scanner.my_ticket)):
            ticket[scanner.assigned_fields[i]] = scanner.my_ticket[i]
        return ticket
        #return {scanner.assigned_fields[i]: scanner.my_ticket[i] for i in range(len(scanner.my_ticket))}

    def setup(self, input_str):
        from operator import itemgetter
        (field_str, my_ticket_str, nearby_ticket_str) = input_str.split('\n\n')
        for line in field_str.splitlines():
            name, lo1, hi1, lo2, hi2 = re.match(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', line).groups()
            self.fields[name] = ([int(lo1), int(hi1)],[int(lo2), int(hi2)])
        self.my_ticket = tuple(list(map(int, my_ticket_str.splitlines()[1].split(','))))
        for line in nearby_ticket_str.splitlines():
            if line == 'nearby tickets:':
                continue
            nums = tuple(list(map(int, line.split(','))))
            self.nearby_tickets.append(nums)

        # Merge all ranges on the fields to a set of valid ranges
        all_ranges = []
        for ranges in self.fields.values():
            all_ranges.extend(ranges)
        all_ranges.sort(key=itemgetter(0, 1))
        cur_range = all_ranges[0].copy()
        for range in all_ranges:
            if range[0] > cur_range[1] + 1:
                # Save current range and start a new one.
                self.valid_ranges.append(cur_range)
                cur_range = range.copy()
            else:
                # Extend range
                if range[1] > cur_range[1]:
                    cur_range[1] = range[1]
        self.valid_ranges.append(cur_range)

    def valid_num(self, num):
        for range in self.valid_ranges:
            if num < range[0]:
                return False
            if num <= range[1]:
                return True
        return False

    def discard_invalid_tickets(self):
        valid_tickets =[]
        for ticket in self.nearby_tickets:
            if reduce(lambda x, y: x & y, map(self.valid_num, ticket)):
                valid_tickets.append(ticket)
        self.nearby_tickets = valid_tickets

    def assign_fields(self):
        poss_fields = [set(list(self.fields.keys())) for x in self.fields.keys()]
        for ticket in self.nearby_tickets:
            for idx, val in enumerate(ticket):
                for key in list(poss_fields[idx]):
                    ranges = self.fields[key]
                    if val < ranges[0][0] or val > ranges[1][1] or ranges[0][1] < val < ranges[1][0]:
                        poss_fields[idx].remove(key)
                        if len(poss_fields[idx]) == 0:
                            raise RuntimeError('Field no longer valid')
        # At this point, if we know that a field is of a given type, we can remove it
        # from contention elsewhere.
        poss_sum = sum([len(x) for x in poss_fields])
        while poss_sum > len(poss_fields):
            self.remove_singletons(poss_fields)
            new_poss_sum = sum([len(x) for x in poss_fields])
            if new_poss_sum == poss_sum:
                raise RuntimeError('I have reached an impasse')
            poss_sum = new_poss_sum
        self.assigned_fields = [next(iter(x)) for x in poss_fields]

    def remove_singletons(self, poss_fields):
        for i, poss_set in enumerate(poss_fields):
            if len(poss_set) == 1:
                (removal_key,) = poss_set
                for j, other_poss_set in enumerate(poss_fields):
                    if i != j and removal_key in other_poss_set:
                        other_poss_set.remove(removal_key)


assert TicketScanner.scan_for_errors('''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12''') == 71
print('16a: ',  TicketScanner.scan_for_errors(data))

assert TicketScanner.parse_my_ticket('''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9''') == {'class': 12, 'row': 11, 'seat': 13}
my_ticket = TicketScanner.parse_my_ticket(data)
dep_fields = []
for key in my_ticket.keys():
    if key.startswith('departure'):
        dep_fields.append(key)
print('16b: ', reduce(lambda x, y: x * y, [my_ticket[x] for x in dep_fields]))