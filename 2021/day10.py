from sre_constants import CATEGORY_NOT_SPACE
from aocd import lines
import re

bad_delim_values = {')': 3, ']': 57, '}': 1197, '>': 25137}

def score_corrupt(lines):
    count = 0
    for line in lines:
        corrupt = corruption(remove_matching_groups(line))
        if corrupt:
            count += bad_delim_values[corrupt]
    return count

def corruption(unmatched_line):
    match = re.search('\>|\]|\}|\)', unmatched_line)
    if match == None:
        return ''
    return match.group(0)
    
def remove_matching_groups(line):
    while True:
        x = re.sub(r'<>|\[\]|\{\}|\(\)', '', line)
        if x == line:
            return line
        line = x

test = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
assert(score_corrupt(test.splitlines())) == 26397
print('10a: ', score_corrupt(lines))

def score_incomplete(lines):
    count = 0
    scores = list(sorted([score_line(x) for x in [remove_matching_groups(l) for l in lines] if not corruption(x)]))
    return scores[len(scores) // 2]

matching_score = {'(': 1, '[': 2, '{': 3, '<': 4}
good_delims = ')]}>'
def score_line(line):
    cnt = 0
    for x in line[::-1]:
        cnt = cnt * 5 + matching_score[x]
    return cnt

assert(score_incomplete(test.splitlines())) == 288957
print('10b: ', score_incomplete(lines))
