from aocd import data
import re

def height_check(value):
    match = re.match(r'^(\d+)(in|cm)$', value)
    if match is None: return False
    length, units = match.groups()
    if units == 'cm':
        return 150 <= int(length) <= 193
    return 59 <= int(length) <= 76

optional_fields = {'cid'}
field_validators = {
    'byr': lambda x: 1920 <= int(x) <= 2002,
    'iyr': lambda x: 2010 <= int(x) <= 2020,
    'eyr': lambda x: 2020 <= int(x) <= 2030,
    'hgt': height_check,
    'hcl': lambda x: re.match(r'^#[0-9a-f]{6}$', x) is not None,
    'ecl': lambda x: re.match(r'^(amb|blu|brn|gry|grn|hzl|oth)$', x) is not None,
    'pid': lambda x: re.match(r'^\d{9}$', x) is not None,
}
required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

def check_passport(passport):
    found_fields = set()
    for field in passport.split():
        name, value = re.match(r'(\w+):(\S+)', field).groups()
        found_fields.add(name)
        if name in field_validators.keys():
            if not field_validators[name](value):
                return False
    diff_with_required = required_fields - found_fields
    diff_with_all = (required_fields | optional_fields) - found_fields
    return diff_with_required == set() or diff_with_all == set()


def check_passports(input):
    count_valid = 0
    for pp in input.split('\n\n'):
        if check_passport(pp):
            count_valid += 1
    return count_valid


test_input = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''
assert check_passports(test_input) == 2

print(f'valid passports: {check_passports(data)}')

test_input2 = '''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
'''
assert check_passports(test_input2) == 4

