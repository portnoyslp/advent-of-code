#!/usr/bin/python
import re

def validPassword(pw):
    # six-digits
    if pw < 100000 or pw > 999999:  return False
    # digits always increase
    pwStr = str(pw)
    sortedPw = ''.join(sorted(pwStr))
    if sortedPw != pwStr: return False
    # has a double digit, but not only 3+-repeats.
    p = re.compile(r'(\d)\1+')
    doubles = 0
    for m in p.finditer(pwStr):
        if len(m.group(0)) == 2:
            doubles += 1
    if doubles == 0: return False
    return True

if validPassword(111111): print("111111 should no longer be good")
if validPassword(223450): print("223450 should be bad")
if validPassword(123789): print("123789 should be bad")
if not validPassword(112233): print("112233 should be good")
if validPassword(123444): print("123444 should be bad")
if not validPassword(111122): print("111122 should be good")

# Check range
count = 0
for pw in range(265275, 781585): # to 265275-781584
    if validPassword(pw): count += 1

print 'Num valid: {}'.format(count)