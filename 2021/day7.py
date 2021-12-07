from aocd import lines
from statistics import median_low

def sum_of_differences(inputstr):
    data = list(map(int, inputstr.split(',')))
    median = median_low(data)
    dists = list(map(lambda x: abs(x - median), data))
    return sum(dists)

assert(sum_of_differences('16,1,2,0,4,2,7,1,2,14')) == 37
print('7a: ', sum_of_differences(lines[0]))

def best_energy(inputstr):
    data = list(map(int, inputstr.split(',')))
    # intial guess
    best_guess = median_low(data)
    optimum = eval_position(data, best_guess)
    while True:
        guess = best_guess + 1
        val = eval_position(data, guess)
        if optimum < val:
            break;
        best_guess = guess
        optimum = val 
    while True:
        guess = best_guess - 1
        val = eval_position(data, guess)
        if optimum < val:
            break;
        best_guess = guess
        optimum = val
    return optimum

def eval_position(data, pos):
    energy = list(map(lambda n: n*(n+1)//2, map(lambda x: abs(x - pos), data)))
    return sum(energy)

assert(best_energy('16,1,2,0,4,2,7,1,2,14')) == 168
print('7a: ', best_energy(lines[0]))
