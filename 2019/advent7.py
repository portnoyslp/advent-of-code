import intcode
import itertools

def run_amplifiers(amp_program_str, phases):
    memory = list(map(int, amp_program_str.split(',')))
    inputVal = 0
    for phase in phases:
        machine = intcode.Intcode(memory)
        output = machine.run_machine([phase, inputVal])
        inputVal = output[0]
    return inputVal


assert run_amplifiers('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', [4, 3, 2, 1, 0]) == 43210
assert run_amplifiers('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0',
                      [0, 1, 2, 3, 4]) == 54321
assert run_amplifiers(
    '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0',
    [1, 0, 4, 3, 2]) == 65210

amp_program_str = '3,8,1001,8,10,8,105,1,0,0,21,34,47,72,81,102,183,264,345,426,99999,3,9,102,5,9,9,1001,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,3,9,4,9,99,3,9,102,3,9,9,101,2,9,9,102,5,9,9,1001,9,3,9,1002,9,4,9,4,9,99,3,9,101,5,9,9,4,9,99,3,9,101,3,9,9,1002,9,5,9,101,4,9,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99'
best_output = 0
best_perm = []
for perm in itertools.permutations([0,1,2,3,4]):
    output = run_amplifiers(amp_program_str, perm)
    if output > best_output:
        best_output = output
        best_perm = perm
print(f"7a answer best output {best_output} ({best_perm})")

def run_amplifiers_feedback_loop(amp_program_str, phases):
    memory = list(map(int, amp_program_str.split(',')))
    # setup amps
    amps = []
    for phase in phases:
        machine = intcode.Intcode(memory)
        machine.input(phase)
        amps.append(machine)
    current_output = 0
    final_output = 0
    while current_output != None:
        final_output = current_output
        amp = amps[0]
        amp.input(current_output)
        current_output = amp.execute()
        # rotate amps
        amps = amps[1:] + amps[:1]
    return final_output

assert run_amplifiers_feedback_loop(
    '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', [9,8,7,6,5]) == 139629729
assert run_amplifiers_feedback_loop(
    '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10', [9,7,8,5,6]) == 18216
best_output = 0
best_perm = []
for perm in itertools.permutations([5,6,7,8,9]):
    output = run_amplifiers_feedback_loop(amp_program_str, perm)
    if output > best_output:
        best_output = output
        best_perm = perm
print(f"7b answer best output {best_output} ({best_perm})")
