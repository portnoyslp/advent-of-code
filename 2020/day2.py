import re
from aocd import data


class PasswordChecker:
    def __init__(self):
        pass

    def valid_password(self, line):
        try:
            low, high, needed_char, pw = self.parse_line(line)
            count = pw.count(needed_char)
            return low <= count <= high
        except RuntimeWarning:
            return False

    @staticmethod
    def parse_line(line):
        match = re.match(r'(\d+)-(\d+) (.): (.+)', line)
        if match is None:
            raise RuntimeWarning('No matches found')
        p1, p2, needed_char, pw = match.groups()
        return int(p1), int(p2), needed_char, pw

    @classmethod
    def count_valid(cls, input_set):
        ok_words = 0
        for line in input_set.splitlines():
            if cls().valid_password(line):
                ok_words += 1
        return ok_words


class NewPasswordChecker(PasswordChecker):
    def valid_password(self, line):
        try:
            pos1, pos2, needed_char, pw = self.parse_line(line)
            chars = [pw[i - 1] for i in [pos1, pos2]]
            return chars.count(needed_char) == 1
        except RuntimeWarning:
            return False


test_input = '''
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''
assert PasswordChecker.count_valid(test_input) == 2
print(f"2a: {PasswordChecker.count_valid(data)}")

assert NewPasswordChecker.count_valid(test_input) == 1
print(f"2b: {NewPasswordChecker.count_valid(data)}")
