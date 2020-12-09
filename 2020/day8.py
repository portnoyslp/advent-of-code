from aocd import data

instructions = []

def create_instructions(input):
    global instructions
    instructions = []
    for instruction in input.splitlines():
        op, val = instruction.split()
        instructions.append([op, int(val)])

def run():
    global instructions
    instruction_idx_run = set()
    accumulator = 0
    ip = 0
    while True:
        if ip in instruction_idx_run:
            return False, accumulator
        if ip >= len(instructions):
            return True, accumulator
        instruction_idx_run.add(ip)
        op, val = instructions[ip]
        if op == 'nop':
            ip += 1
        elif op == 'jmp':
            ip += val
        elif op == 'acc':
            accumulator += val
            ip += 1
        else:
            raise RuntimeError(f'Unexpected op: {op}')

def run_until_loop():
    terminated, accumulator = run()
    return accumulator


test_bootcode = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''
create_instructions(test_bootcode)
assert run_until_loop() == 5

create_instructions(data)
print(f'8a: {run_until_loop()}')

def alter_bootcode_until_terminates():
    # Go through instructions, and try swapping nop/jmp until we get a terminating loop
    for ip in range(len(instructions)):
        old_op = instructions[ip][0]
        if old_op == 'acc':
            continue
        instructions[ip][0] = 'jmp' if old_op == 'nop' else 'nop'
        # test
        terminated, accumulator = run()
        if terminated:
            return accumulator
        # reset
        instructions[ip][0] = old_op
    raise RuntimeError('Couldn\'t fix code')

create_instructions(test_bootcode)
assert alter_bootcode_until_terminates() == 8

create_instructions(data)
print(f'8b: {alter_bootcode_until_terminates()}')

