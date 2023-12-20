from aocd import data
import re
from functools import reduce

class Workflows:
    def __init__(self, data) -> None:
        self.workflows = {}
        self.ratings = []

        workflow_list,rating_list = data.split('\n\n')
        for workflow in workflow_list.splitlines():
            rules = []
            label,rule_list = re.match('(\w+){(.*)}', workflow).groups()
            for rule in rule_list.split(','):
                if ':' in rule:
                    rules.append(tuple(rule.split(':')))
                else:
                    rules.append(rule)
            self.workflows[label] = rules
        
        for rating in rating_list.splitlines():
            rdict = {}
            for assignment in rating[1:-1].split(','):
                rdict[assignment[0]] = int(assignment[2:])
            self.ratings.append(rdict)

    def exec_ruleset(self, rules, rating):
        for rule in rules:
            if type(rule) is tuple:
                b = eval(rule[0], None, rating)
                if b:
                    return rule[1]
            else:
                return rule
        return None # shouldn't happend

    def acceptable(self,rating):
        flowname = 'in'
        while True:
            rules = self.workflows[flowname]
            flowname = self.exec_ruleset(rules, rating)
            if flowname == 'R':
                return False
            elif flowname == 'A':
                return True

    def run_ratings(self):
        total = 0
        for rating in self.ratings:
            if self.acceptable(rating):
                lst = list(rating.values())
                total += sum(rating.values())
        return total
    
    def acceptable_combos_for_rules(self, rules, ranges):
        if len(rules) == 0:
            return None # shouldn't occur
        
        rule = rules[0]
            
        if type(rule) is tuple:
            var, op, val = re.match('(.)([<|>])(\d+)', rule[0]).groups()
            true_ranges = ranges.copy()
            false_ranges = ranges.copy()
            r = ranges[var]
            if op == '<':
                true_ranges[var] = (r[0], int(val) - 1)
                false_ranges[var] = (int(val), r[1])
            else:
                true_ranges[var] = (int(val) + 1, r[1])
                false_ranges[var] = (r[0], int(val))
            return (self.acceptable_combos_for_flow(rule[1], true_ranges) + 
                    self.acceptable_combos_for_rules(rules[1:], false_ranges))
        return self.acceptable_combos_for_flow(rule, ranges)

    def acceptable_combos_for_flow(self, flowname, ranges):
        if flowname == 'R':
            return 0
        if flowname == 'A':
            return reduce(lambda x,y:x*y, [x[1]-x[0]+1 for x in ranges.values()])

        rules = self.workflows[flowname]
        return self.acceptable_combos_for_rules(rules, ranges)

    def count_combos(self):
        ranges = {'x': (1,4000), 'm': (1,4000), 'a': (1,4000), 's': (1,4000)}
        flowname = 'in'
        return self.acceptable_combos_for_flow('in', ranges)

        
def run(data, part=1):
    workflows = Workflows(data)
    if part == 1:
        return workflows.run_ratings()
    return workflows.count_combos()

ex1='''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''

assert run(ex1) == 19114
print('19a: ', run(data))
assert run(ex1, part=2) == 167409079868000
print('19b: ', run(data, part=2))