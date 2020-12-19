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
            self.tokens = self.simplify_token_list(self.tokens)
        return int(self.tokens.pop(0))

    def simplify_token_list(self, token_list):
        for i in range(len(token_list) - 2):
            # all ( x ) -> x
            lp, val, rp = token_list[i:i + 3]
            if lp == '(' and rp == ')':
                token_list.pop(i)
                token_list.pop(i + 1)
                return token_list
        for i in range(len(self.tokens) - 2):
            # first num op num -> calculate
            val1, op, val2 = token_list[i:i + 3]
            if self.isnum(val1) and self.isnum(val2) and op in ['*', '+']:
                val1 = int(val1)
                val2 = int(val2)
                del token_list[i:i + 3]
                token_list.insert(i, val1 * val2 if op == '*' else val1 + val2)
                return token_list

    @staticmethod
    def isnum(token):
        return type(token) is int or token[0].isdigit()


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

    def simplify_token_list(self, token_list):
        # If there's a ( num ) -> num
        for i in range(len(token_list) - 2):
            # all ( x ) -> x
            lp, val, rp = token_list[i:i + 3]
            if lp == '(' and rp == ')':
                token_list.pop(i)
                token_list.pop(i + 1)
                return token_list
        # Resolve paren'd equations down to singletons
        token_list, altered = self.resolve_parens(token_list)
        if altered:
            return token_list
        # Resolve + signs
        for i in range(len(token_list) - 2):
            # first num + num -> calculate
            val1, op, val2 = token_list[i:i + 3]
            if self.isnum(val1) and self.isnum(val2) and op == '+':
                val1 = int(val1)
                val2 = int(val2)
                del token_list[i:i + 3]
                token_list.insert(i, val1 + val2)
                return token_list
        # Finally, when we're down to just * signs, handle those
        for i in range(len(token_list) - 2):
            # first num * num -> calculate
            val1, op, val2 = token_list[i:i + 3]
            if self.isnum(val1) and self.isnum(val2) and op == '*':
                val1 = int(val1)
                val2 = int(val2)
                del token_list[i:i + 3]
                token_list.insert(i, val1 * val2)
                return token_list

    def resolve_parens(self, token_list):
        # find innermost parens
        paren_level = []
        cur_level = 0
        for token in token_list:
            if token == '(':
                cur_level += 1
            if token == ')':
                cur_level -= 1
            paren_level.append(cur_level)
        if sum(paren_level) == 0:
            return token_list, False
        max_level = max(paren_level)
        sublist_idx = paren_level.index(max_level)
        sublist_end = paren_level.index(max_level - 1, sublist_idx)
        return token_list[:sublist_idx + 1] + self.simplify_token_list(
            token_list[sublist_idx+1:sublist_end]) + token_list[sublist_end:], True


def process_all2(input_str):
    return sum(map(lambda x: Homework2().process(x), input_str.splitlines()))


assert Homework2().process('1 + 2 * 3 + 4 * 5 + 6') == 231
assert Homework2().process('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert Homework2().process('2 * 3 + (4 * 5)') == 46
assert Homework2().process('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert Homework2().process('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert Homework2().process('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340
print('18b: ', process_all2(data))

# PLY Lexer version
import ply.yacc as yacc
import ply.lex as lex

tokens = ('NUMBER', 'OPEN', 'CLOSE', 'PLUS', 'MUL')
t_PLUS = r'\+'
t_MUL = r'\*'
t_OPEN = r'\('
t_CLOSE = r'\)'
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Oopsie: Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore = ' '
lexer = lex.lex()

# Parsing
precedence = (('left', 'MUL'), ('left', 'PLUS'))

def p_expression_group(t):
    'expression : OPEN expression CLOSE'
    t[0] = t[2]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MUL expression'''
    if t[2] == '+' : t[0] = t[1] + t[3]
    elif t[2] == '*' : t[0] = t[1] * t[3]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_error(t):
    print("Oopsie: syntax error at '%s'" % t.value)

parser = yacc.yacc()
def parse_input(input_str):
    return parser.parse(input_str)

assert parse_input('1 + 2 * 3 + 4 * 5 + 6') == 231
assert parse_input('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert parse_input('2 * 3 + (4 * 5)') == 46
assert parse_input('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert parse_input('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert parse_input('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

print('18b (parser): ', sum(map(parse_input, data.splitlines())))


