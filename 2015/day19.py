from aocd import data

created_molecules = set()


def replace(rule, molecule):
    idx = 0
    if rule.find(' => ') == -1:
        return
    src, dest = rule.split(' => ')
    while idx != -1 and idx < len(molecule):
        idx = molecule.find(src, idx)
        if idx != -1:
            created_molecules.add(molecule[:idx] + dest + molecule[idx + len(src):])
            idx += 1


rules = data.splitlines()
molecule = rules[-1]
rules = rules[:-1]
for rule in rules:
    replace(rule, molecule)

print('19a: ', len(created_molecules))
