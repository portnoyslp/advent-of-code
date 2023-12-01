from aocd import data
import re

numwords = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

def calibrate(data, part=1):
    digits = '\d'
    if part == 2:
        digits = '\d|' + '|'.join(numwords.keys())
 
    sum = 0
    for line in data.splitlines():
        first = re.match('.*?(' + digits + ')', line).group(1)
        second = re.match('.*(' + digits + ').*?$', line).group(1)
        num = int(translate(first) + translate(second))
        sum += num
    return sum

def translate(num_or_word):
    if len(num_or_word) > 1:
        return numwords[num_or_word]
    return num_or_word

ex1 = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''

assert calibrate(ex1) == 142
print('1a: ', calibrate(data))

ex2 = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
assert calibrate(ex2, 2) == 281
print ('1b: ', calibrate(data, 2))