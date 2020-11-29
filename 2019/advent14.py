from collections import defaultdict


def parse_formula(formula_str):
    # Format is (QUANT CHEMICAL)* => QUANT CHEMICAL
    (inputs, output) = formula_str.split(' => ')
    (quantity_created, output_chem) = output.split(' ')
    req_list = []
    for input in inputs.split(', '):
        (quantity_needed, input_chem) = input.split(' ')
        req_list.append([int(quantity_needed), input_chem])
    return output_chem, int(quantity_created), req_list


def ceil_div(a, b):
    return -(-a // b)


class OutOfOreException(Exception):
    pass


class ChemicalCalculator:
    def __init__(self, formulae_str):
        # formula dict links from chemical name to a tuple of quantity_created, and a list of requirements.
        # Requirements are a tuple of the quantity required, as well as the input chemical.
        self.formula_dict = {}
        for formula in formulae_str.splitlines():
            if formula == '':
                continue
            (output_chem, quantity_created, req_list) = parse_formula(formula)
            self.formula_dict[output_chem] = (quantity_created, req_list)
        self.initial_ore = 1000000000000
        self.storehouse = defaultdict(int)
        self.reset_ore()
        self.required = {}

    def reset_ore(self):
        self.storehouse['ORE'] = self.initial_ore

    def process_requirement(self, req_chemical):
        # Remove from requirement list
        needed = self.required[req_chemical]
        del self.required[req_chemical]
        # This shouldn't be necessary, but just in case we have it on hand
        needed = self.extract_from_stores(needed, req_chemical)
        # Find the equation that makes it
        (quantity_created, req_list) = self.formula_dict[req_chemical]
        # Number of times we need to repeat this formula
        formula_reps = ceil_div(needed, quantity_created)
        leftover = quantity_created * formula_reps - needed
        # Leftovers get stored
        self.storehouse[req_chemical] += leftover
        # Add to requirements
        for (quantity_needed, chemical) in req_list:
            quantity_needed *= formula_reps
            quantity_needed = self.extract_from_stores(quantity_needed, chemical)
            if quantity_needed > 0 and chemical == 'ORE':
                raise OutOfOreException('No more ore')
            if chemical in self.required.keys():
                self.required[chemical] += quantity_needed
            else:
                self.required[chemical] = quantity_needed

    def extract_from_stores(self, needed, req_chemical):
        # Get what we need from available stores
        available = self.storehouse[req_chemical]
        if available > needed:
            self.storehouse[req_chemical] -= needed
            needed = 0
        else:
            needed -= available
            self.storehouse[req_chemical] = 0
        return needed

    def calculate_fuel(self, fuel_desired=1):
        self.required['FUEL'] = fuel_desired
        # Process until we only have ORE required
        while not all(chem == 'ORE' for chem in self.required.keys()):
            chemical = next(filter(lambda c: c != 'ORE', self.required.keys()))
            self.process_requirement(chemical)
        return self.initial_ore - self.storehouse['ORE']


assert ChemicalCalculator("""
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""").calculate_fuel() == 31

small_test_formulae = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""
assert ChemicalCalculator(small_test_formulae).calculate_fuel() == 13312

medium_test_formulae = """
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""
assert ChemicalCalculator(medium_test_formulae).calculate_fuel() == 180697

large_test_formulae = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""
assert ChemicalCalculator(large_test_formulae).calculate_fuel() == 2210736

real_input = """
4 BFNQL => 9 LMCRF
2 XGWNS, 7 TCRNC => 5 TPZCH
4 RKHMQ, 1 QHRG, 5 JDSNJ => 4 XGWNS
6 HWTBC, 4 XGWNS => 6 CWCD
1 BKPZH, 2 FLZX => 9 HWFQG
1 GDVD, 2 HTSW => 8 CNQW
2 RMDG => 9 RKHMQ
3 RTLHZ => 3 MSKWT
1 QLNHG, 1 RJHCP => 3 GRDJ
10 DLSD, 2 SWKHJ, 15 HTSW => 1 TCRNC
4 SWKHJ, 24 ZHDSD, 2 DLSD => 3 CPGJ
1 SWKHJ => 1 THJHK
129 ORE => 8 KLSMQ
3 SLNKW, 4 RTLHZ => 4 LPVGC
1 SLNKW => 5 RLGFX
2 QHRG, 1 SGMK => 8 RJHCP
9 RGKCF, 7 QHRG => 6 ZHDSD
8 XGWNS, 1 CPGJ => 2 QLNHG
2 MQFJF, 7 TBVH, 7 FZXS => 2 WZMRW
13 ZHDSD, 11 SLNKW, 18 RJHCP => 2 CZJR
1 CNQW, 5 GRDJ, 3 GDVD => 4 FLZX
129 ORE => 4 RHSHR
2 HWTBC, 2 JDSNJ => 8 QPBHG
1 BKPZH, 8 SWKHJ => 6 WSWBV
8 RJHCP, 7 FRGJK => 1 GSDT
6 QPBHG => 4 BKPZH
17 PCRQV, 6 BFNQL, 9 GSDT, 10 MQDHX, 1 ZHDSD, 1 GRDJ, 14 BRGXB, 3 RTLHZ => 8 CFGK
8 RMDG => 6 SGMK
3 CZJR => 8 RTLHZ
3 BFRTV => 7 RGKCF
6 FRGJK, 8 CZJR, 4 GRDJ => 4 BRGXB
4 VRVGB => 7 PCRQV
4 TCRNC, 1 TBVH, 2 FZXS, 1 BQGM, 1 THJHK, 19 RLGFX => 2 CRJTJ
5 RDNJK => 6 SWKHJ
2 FLVC, 2 SLNKW, 30 HWTBC => 8 DLSD
6 TBVH, 3 ZHDSD => 5 BQGM
17 RLGFX => 4 SCZQN
8 SWKHJ => 6 FZXS
9 LZHZ => 3 QDCL
2 ZHDSD => 1 RDNJK
15 FZXS, 3 TPZCH => 6 MQFJF
12 RLGFX, 9 QPBHG, 6 HTSW => 1 BFNQL
150 ORE => 9 BFRTV
2 BFRTV, 2 KLSMQ => 2 RMDG
4 VFLNM, 30 RKHMQ, 4 CRJTJ, 24 CFGK, 21 SCZQN, 4 BMGBG, 9 HWFQG, 34 CWCD, 7 LPVGC, 10 QDCL, 2 WSWBV, 2 WTZX => 1 FUEL
6 RHSHR, 3 RGKCF, 1 QHRG => 6 JDSNJ
3 MQDHX, 2 XGWNS, 12 GRDJ => 9 LZHZ
128 ORE => 6 ZBWLC
9 JDSNJ, 7 RMDG => 8 FLVC
4 DLSD, 12 CZJR, 3 MSKWT => 4 MQDHX
2 BXNX, 4 ZBWLC => 3 QHRG
19 LMCRF, 3 JDSNJ => 2 BMGBG
1 RJHCP, 26 SGMK => 9 HTSW
2 QPBHG => 8 VFLNM
2 RGKCF => 9 SLNKW
3 LZHZ, 2 GRDJ => 2 TBVH
100 ORE => 2 BXNX
4 DLSD, 21 JDSNJ => 8 GDVD
2 QHRG => 2 HWTBC
1 LPVGC, 8 XGWNS => 8 FRGJK
9 FZXS => 7 VRVGB
7 WZMRW, 1 TBVH, 1 VFLNM, 8 CNQW, 15 LZHZ, 25 PCRQV, 2 BRGXB => 4 WTZX
"""

ore_required = ChemicalCalculator(real_input).calculate_fuel()
print(f"14a ore required = {ore_required}")


#### 14b
def fuel_possible(formula_str):
    calc = ChemicalCalculator(formula_str)
    # Get ore required per fuel. This is an overestimate, since later fuel will be able to reuse
    # stored byproducts.
    ore_per_fuel = calc.calculate_fuel()
    calc.reset_ore()
    # Continually try to get the max amount of fuel by the calculation, then keep adding more fuel to the fire
    # until we run out of ore.
    fuel_gathered = 0
    while True:
        fuel_amount = calc.storehouse['ORE'] // ore_per_fuel
        if fuel_amount < 1:
            fuel_amount = 1
        try:
            calc.calculate_fuel(fuel_amount)
            fuel_gathered += fuel_amount
        except OutOfOreException:
            break
    return fuel_gathered


assert fuel_possible(small_test_formulae) == 82892753
assert fuel_possible(medium_test_formulae) == 5586022
assert fuel_possible(large_test_formulae) == 460664

print(f"14b possible fuel = {fuel_possible(real_input)}")
# For some reason, the actual answer was one less than this; I'm not sure why.
