from aocd import lines

def spot_check(inputlines):
    num_segs_1478 = [2,4,3,7]
    count_1478 = 0
    for line in inputlines:
        (digits, output) = line.split(' | ')
        for output_word in output.split():
            if len(output_word) in num_segs_1478:
                count_1478 += 1
    return count_1478

test = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''
assert(spot_check(test.splitlines())) == 26
print('8a: ', spot_check(lines))


def decode(inputlines):
    return sum([decode_line(l) for l in inputlines])

expected_segments = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

        
def decode_line(line):
    (digits, output) = line.split(' | ')
    ds = sorted(map(set,digits.split()), key=lambda x: len(x))
    output_sets = map(set, output.split())

    mapping = {}
    # ds are the digit sets, sorted by length, so we know that 
    # ds[0] == "1", ds[1] = "7", ds[2] = "4", ds[3-5] = {2,3,5}, ds[6-8] = {0,6,9}, and ds[9] is "8".
    mapping[mkey(ds[0])] = 1
    mapping[mkey(ds[1])] = 7
    mapping[mkey(ds[2])] = 4
    mapping[mkey(ds[9])] = 8

    # But what are the others? Well, 3 is basically the element in 3-5 that overlaps twice with 1, and 2 overlaps with 4 in 2 spots.
    for idx in range(3,6):
        if len(ds[0].intersection(ds[idx])) == 2:
            mapping[mkey(ds[idx])] = 3
            index_3 = idx
        elif len(ds[2].intersection(ds[idx])) == 2:
            mapping[mkey(ds[idx])] = 2
        else:
            mapping[mkey(ds[idx])] = 5
            index_5 = idx
    
    # This is the fun one. 9 is the union of 1 and 5, and 6 is what you get when you take a 5 and union it with the difference of 8 and 3.
    nine_set = ds[index_5].union(ds[0])
    six_set = ds[index_5].union(ds[9].difference(ds[index_3]))
    for idx in range(6,9):
        if ds[idx] == nine_set:
            mapping[mkey(ds[idx])] = 9
        elif ds[idx] == six_set:
            mapping[mkey(ds[idx])] = 6
        else:
            mapping[mkey(ds[idx])] = 0
    
    # And now we should be able to translate the output digits.
    return int(''.join(map(lambda x: str(mapping[mkey(x)]), output_sets)))

def mkey(set):
    return tuple(sorted(set))


assert(decode(test.splitlines())) == 61229
print('8b: ', decode(lines))
