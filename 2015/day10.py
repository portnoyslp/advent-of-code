from itertools import groupby


def look_and_say(x):
    output = ''
    for k, g in groupby(x):
        output += str(len(list(g))) + str(k)
    return output


def iter(start, cnt):
    for i in range(cnt):
        start = look_and_say(start)
    return start


assert iter('1', 5) == '312211'
print('10a: ', len(iter('1113222113', 40)))

print('10b: ', len(iter('1113222113', 50)))
