from aocd import data
import re
import math

monkeys = []
monkeys_lcm = 1

class Monkey:
    def __init__(self, data, part=1):
        self.num = int(re.match('Monkey (\d+):', data).group(1))
        start_items = re.search('Starting items: ([\d, ]+)', data).group(1)
        self.items = [int(x) for x in start_items.split(', ')]
        self.operation = re.search('Operation: new = (.*)', data).group(1)
        self.test_div = int(re.search('Test: divisible by (\d+)', data).group(1))
        self.monkey_true = int(re.search('If true: throw to monkey (\d+)', data).group(1))        
        self.monkey_false = int(re.search('If false: throw to monkey (\d+)', data).group(1))
        self.exam_count = 0
        self.part = part
    
    def summary(self):
        print('Monkey {}: {}'.format(self.num, ', '.join([str(x) for x in self.items])))

    def catch_item(self, item):
        self.items.append(item)
    
    def process_items(self):
        for item in self.items:
            self.exam_count += 1
            worry = item
            worry = eval(self.operation, None, {'old': worry})
            if self.part == 1:
                worry = worry // 3
            else:
                worry = worry % monkeys_lcm
            result = worry % self.test_div
            if result == 0:
                monkeys[self.monkey_true].catch_item(worry)
            else:
                monkeys[self.monkey_false].catch_item(worry)
        self.items = []


def run_monkeys():
    for monkey in monkeys:
        monkey.process_items()
            
def build_monkeys(data, part=1):
    global monkeys, monkeys_lcm
    monkeys = [Monkey(chunk, part) for chunk in data.split('\n\n')]
    monkeys_lcm = math.prod([m.test_div for m in monkeys])

    
def monkey_business(data, part=1):
    build_monkeys(data, part)
    limit = 20 if part == 1 else 10000
    for round in range(limit):
        run_monkeys()
    
    monkeys.sort(key = lambda m:m.exam_count, reverse = True)
    return monkeys[0].exam_count * monkeys[1].exam_count
        

ex1 = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''

assert(monkey_business(ex1) == 10605)
print('11a: ', monkey_business(data))
assert(monkey_business(ex1, part=2) == 2713310158)
print('11b: ', monkey_business(data, part=2))
