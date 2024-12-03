from aocd import data

def safe_reports(data, part=1):
    cnt = 0
    for report in data.splitlines():
        orig = map(int, report.split())
        if part == 1 and safe_report(orig):
            cnt += 1
        if part == 2:
            # copy report, and try removing each value in turn.
            orig = list(orig)
            for i in range(len(orig)):
                c = orig.copy()
                c.pop(i)
                if safe_report(c):
                    cnt += 1
                    break
    return cnt

def safe_report(report):
    dir = 0
    prev_val = "xxx"
    for val in report:
        if prev_val != "xxx":
            if (val - prev_val < 0 and dir > 0):
                return False
            if (val - prev_val > 0 and dir < 0):
                return False
            if (val - prev_val > 3 or val - prev_val < -3):
                return False
            if (val == prev_val):
                return False
            dir = val - prev_val
        prev_val = val
    return True


ex1 = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''

assert safe_reports(ex1) == 2
print('2a: ', safe_reports(data))
assert safe_reports(ex1, part=2) == 4
print('2a: ', safe_reports(data, part=2))