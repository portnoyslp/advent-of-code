from aocd import data
import re

class Homework:
    def __init__(self):
        self.tokens = []
        self.baseptr = 0

    def process(self, input):
        while input != '':
            token, input = re.match(r'^(\d+|[*+()]) ?(.*)', input).groups()
            self.tokens.append(token)
        return self.process_tokens()

    def process_tokens(self):
        while len(self.tokens) > 1:
            self.process_top_operation()
        return int(self.tokens.pop(0))

    def process_top_operation(self):
        val1 = self.fetch_operand()
        op = self.fetch_op()
        val2 = self.fetch_operand()
        self.tokens.insert(0, val1 * val2 if op == '*' else val1 + val2)

    def fetch_op(self):
        return self.tokens.pop(0)

    def fetch_operand(self):
        if self.tokens[0] == '(':
            # process parens
            self.tokens.pop(0)
            while self.tokens[1] != ')':
                self.process_top_operation()
            self.tokens.pop(1)
        return int(self.tokens.pop(0))

def process_all(input_str):
    return sum(map(lambda x: Homework().process(x), input_str.splitlines()))


assert Homework().process('1 + 2 * 3 + 4 * 5 + 6') == 71
assert Homework().process('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert Homework().process('2 * 3 + (4 * 5)') == 26
assert Homework().process('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert Homework().process('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert Homework().process('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632
print('18a: ', process_all(data))

class Homework2(Homework):
    def __init__(self):
        Homework.__init__(self)



def process_all2(input_str):
    return sum(map(lambda x: Homework2().process(x), input_str.splitlines()))

assert Homework2().process('1 + 2 * 3 + 4 * 5 + 6') == 231
assert Homework2().process('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert Homework2().process('2 * 3 + (4 * 5)') == 46
assert Homework2().process('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert Homework2().process('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert Homework2().process('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340
print('18a: ', process_all2(data))
