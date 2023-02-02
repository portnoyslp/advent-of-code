from aocd import lines

rps_scores = {'R': 1, 'P': 2, 'S': 3}
outcome_scores = {'W': 6, 'D': 3, 'L': 0}
outcomes = {'RR':'D','PP':'D','SS':'D','RS':'W','SP':'W','PR': 'W','SR':'L','PS':'L','RP':'L'} 
decrypt = {'A': 'R', 'B': 'P', 'C': 'S', 'X': 'R', 'Y': 'P', 'Z': 'S'}
decrypt_p2 = {'A': 'R', 'B': 'P', 'C': 'S', 'X': 'L', 'Y': 'D', 'Z': 'W'}
def eval_move(line, part=1):
    codebook = decrypt
    if (part == 2):
        codebook = decrypt_p2
    
    m1, m2 = line.split()
    m1 = codebook[m1]
    m2 = codebook[m2]
    
    if part == 1:
        return rps_scores[m2] + outcome_scores[outcomes[m2 + m1]]
    
    # find play with outcome that matches m2.
    for play in ['R','P','S']:
        if outcomes[play + m1] == m2:
            return rps_scores[play] + outcome_scores[m2]
    return -1 # shouldn't happen

def eval_games(lines, part=1):
    tot = 0
    for line in lines:
        tot += eval_move(line, part)
    return tot

ex1 = """A Y
B X
C Z
"""
assert eval_games(ex1.splitlines()) == 15
print('2a: ', eval_games(lines))

assert eval_games(ex1.splitlines(), part=2) == 12
print('2b: ', eval_games(lines, part=2)) 

