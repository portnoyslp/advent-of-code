from aocd import lines
from itertools import permutations
import copy

class SnailfishNum:
    def __init__(self, line):
        # treat the line as a basic array, but '[' and ']' are tokens.
        self.ary = []
        for x in line:
            if x == ',':
                continue
            if x >= '0' and x <= '9':
                self.ary.append(int(x))
            else:
                self.ary.append(x)

    def __repr__(self):
        output = 'Snf< ' + self.ary[0]
        last_token = self.ary[0]
        for x in self.ary[1:]:
            if (isinstance(x, int) and last_token != '[') or (x == '[' and last_token != '['):
                output += ','
            output += str(x)
            last_token = x
        return output + ' >'

    def explode(self):
        # go through array, and keep track of the depth.
        depth = 0
        changed = False
        for idx, x in enumerate(self.ary):
            if x == ']':
                depth -= 1
            if x == '[':
                depth += 1
                if depth >= 5 and isinstance(self.ary[idx+1],int) and isinstance(self.ary[idx+2],int):
                    # OK, this is the start of a tuple that is nested too deeply.
                    # The arg at idx+1 and idx+2 are the tuple values.
                    # We will replace all of [idx : idx + 3] with 0
                    for larg_idx in range(idx-1, 0, -1):
                        if isinstance(self.ary[larg_idx], int):
                            self.ary[larg_idx] += self.ary[idx + 1]
                            break
                    for rarg_idx in range(idx+4,len(self.ary)):
                        if isinstance(self.ary[rarg_idx], int):
                            self.ary[rarg_idx] += self.ary[idx + 2]
                            break
                    self.ary[idx: idx + 4] = [0]
                    changed = True
                    break
        return changed
    
    def ssplit(self):
        for idx, x in enumerate(self.ary):
            if isinstance(x, int) and x > 9:
                self.ary[idx:idx+1] = [ '[', x // 2, (x+1)//2, ']' ]
                return True
        return False

    def reduce(self):
        changed = True
        while changed:
            changed = self.explode()
            changed = changed or self.ssplit()

    def __add__(self, y):
        self.ary= ['['] + self.ary + y.ary + [']']
        self.reduce()
        return self
    
    def magnitude(self):
        temp_list = self.ary.copy()
        while len(temp_list) > 1:
            for idx, x in enumerate(temp_list[0:-2]):
                if isinstance(x, int) and isinstance(temp_list[idx+1], int):
                    # this is a pair, replace it and the surrounding brackets with the calc'd magnitude
                    magnitude = 3 * x + 2 * temp_list[idx+1]
                    temp_list[idx - 1: idx + 3] = [magnitude]
                    break
        return temp_list[0]

assert(SnailfishNum('[[1,2],[[3,4],5]]').magnitude() == 143)

def magnitude_of_sum(lines):
    accum = SnailfishNum(lines[0])
    for line in lines[1:]:
        addend = SnailfishNum(line)
        accum = accum + addend
    return accum.magnitude()

def magnitude_of_two_nums(lines):
    all_nums = list(map(SnailfishNum, lines))
    highest_magnitude = -1
    best_combo = None
    for (n1,n2) in permutations(all_nums, 2):
        magnitude = (copy.deepcopy(n1)+n2).magnitude()
        if magnitude > highest_magnitude:
            highest_magnitude = magnitude
            best_combo = (n1, n2)
    return highest_magnitude

test="""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""
assert(magnitude_of_sum(test.splitlines()) == 4140)
print('18a: ', magnitude_of_sum(lines))

assert(magnitude_of_two_nums(test.splitlines()) == 3993)
print('18b: ',magnitude_of_two_nums(lines))