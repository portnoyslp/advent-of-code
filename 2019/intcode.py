class Intcode:
    def __init__(self, memory, input_callback = None):
        if type(memory) is str:
            memory = list(map(int, memory.split(',')))
        self.memory = list(memory)
        self.input_values = []
        self.output_values = []
        self.iptr = 0
        self.relative_base = 0
        self.input_callback = input_callback

    class StopException(Exception):
        pass

    def __param_idx(self, idx, param_modes):
        mode = param_modes // 10 ** (idx - 1) % 10
        output_idx = -1
        if mode == 0:
            # position mode
            output_idx = self.memory[self.iptr + idx]
        if mode == 1:
            # immediate
            output_idx = self.iptr + idx
        if mode == 2:
            # relative
            output_idx = self.memory[self.iptr + idx] + self.relative_base
        if output_idx == -1:
            raise NotImplementedError('No such parameter mode %d' % mode)
        # Expand memory to cover referenced index if necessary.
        if len(self.memory) <= output_idx:
            self.memory.extend([0] * (output_idx + 1 - len(self.memory)))
        return output_idx

    def __fetch_param(self, idx, param_modes):
        return self.memory[self.__param_idx(idx, param_modes)]

    def __add(self, param_modes):
        output_idx = self.__param_idx(3, param_modes)
        self.memory[output_idx] = self.__fetch_param(1, param_modes) + self.__fetch_param(2, param_modes)
        self.iptr += 4

    def __mult(self, param_modes):
        output_idx = self.__param_idx(3, param_modes)
        self.memory[output_idx] = self.__fetch_param(1, param_modes) * self.__fetch_param(2, param_modes)
        self.iptr += 4

    def __input(self, param_modes):
        idx = self.__param_idx(1, param_modes)
        if len(self.input_values) == 0:
            if self.input_callback is None:
                raise RuntimeError('Inputing when no input available.')
            self.input_values.append(self.input_callback())
        self.memory[idx] = self.input_values.pop(0)
        self.iptr += 2

    def __output(self, param_modes):
        self.output_values.append(self.__fetch_param(1, param_modes))
        self.iptr += 2

    def __jump_if_true(self, param_modes):
        if self.__fetch_param(1, param_modes) != 0:
            self.iptr = self.__fetch_param(2, param_modes)
        else:
            self.iptr += 3

    def __jump_if_false(self, param_modes):
        if self.__fetch_param(1, param_modes) == 0:
            self.iptr = self.__fetch_param(2, param_modes)
        else:
            self.iptr += 3

    def __less_than(self, param_modes):
        output_idx = self.__param_idx(3, param_modes)
        self.memory[output_idx] = 1 if self.__fetch_param(1, param_modes) < self.__fetch_param(2, param_modes) else 0
        self.iptr += 4

    def __equals(self, param_modes):
        output_idx = self.__param_idx(3, param_modes)
        self.memory[output_idx] = 1 if self.__fetch_param(1, param_modes) == self.__fetch_param(2, param_modes) else 0
        self.iptr += 4

    def __adjust_rbase(self, param_modes):
        self.relative_base += self.__fetch_param(1, param_modes)
        self.iptr += 2

    def __stop(self, param_modes):
        raise Intcode.StopException('STOP')

    operations = {
        1: __add,
        2: __mult,
        3: __input,
        4: __output,
        5: __jump_if_true,
        6: __jump_if_false,
        7: __less_than,
        8: __equals,
        9: __adjust_rbase,
        99: __stop
    }

    def process_opcode(self):
        opcode = self.memory[self.iptr]
        param_modes = opcode // 100
        op = opcode % 100
        if op not in self.operations.keys():
            raise NotImplementedError('No such op %d' % op)
        try:
            self.operations[op](self, param_modes)
        except Intcode.StopException:
            return 'STOP'

    def input(self, arg_or_args):
        if isinstance(arg_or_args, list):
            self.input_values = arg_or_args
        else:
            self.input_values.append(arg_or_args)

    def run_machine(self, input_ary):
        self.input_values = input_ary
        while self.process_opcode() != 'STOP':
            continue
        return self.output_values

    # Run machine until output is ready or until it halts. Returns the output.
    def execute(self):
        while self.process_opcode() != 'STOP':
            if len(self.output_values) > 0:
                break
        if len(self.output_values) == 0:
            # We halted
            return None
        out = self.output_values[0]
        self.output_values = []
        return out
