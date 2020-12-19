from aocd import data
import regex as re
from functools import lru_cache

class Parser:
    def __init__(self, rules_str, part=1):
        self.part = part
        self.rules = {}
        for rule in rules_str.splitlines():
            self.add_rule(rule)
        self.rule_zero = re.compile('^' + self.regexp_for_rule(0) + '$')

    def add_rule(self, rule):
        match = re.match(r'^(\d+): "(.*)"', rule)
        if match:
            rule_num, token = match.groups()
            self.rules[int(rule_num)] = token
        else:
            rule_num, rule_str = re.match(r'^(\d+): (.*)$', rule).groups()
            self.rules[int(rule_num)] = rule_str.split(' ')

    @lru_cache(maxsize=None)
    def regexp_for_rule(self, rule_num):
        rule = self.rules[rule_num]
        if type(rule) == str:
            return rule
        if rule_num == 11 and self.part == 2:
            # Replace two rules with (?P<group>[rule1](?group)[rule2])
            r1 = self.regexp_for_rule(int(rule[0]))
            r2 = self.regexp_for_rule(int(rule[1]))
            return '(?P<group>' + r1 + '(?&group)?' + r2 + ')'
        regexp_str = ''.join(map(lambda x: '|' if x == '|' else self.regexp_for_rule(int(x)), rule))
        if rule_num == 8 and self.part == 2:
            # Replace rule with (rule)+
            return '(' + self.regexp_for_rule(int(rule[0])) + '+)'

        if '|' in rule:
            return '(' + regexp_str + ')'
        return regexp_str

    def test(self, test_str):
        return self.rule_zero.match(test_str) is not None


def run_input(input_str, part=1):
    rules, test_strings = input_str.split('\n\n')
    parser = Parser(rules, part)
    matches = []
    return sum([int(parser.test(x)) for x in test_strings.splitlines()])


test_input = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''
assert run_input(test_input) == 2
print('19a: ', run_input(data))

test_input2 = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''
assert run_input(test_input2) == 3
assert run_input(test_input2, part=2) == 12

print('19b: ', run_input(data, part=2))
