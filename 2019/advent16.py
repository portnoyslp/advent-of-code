import numpy as np
import itertools
from itertools import cycle, accumulate
from aocd import data


class FFT:
    def __init__(self):
        self.base_pattern = [0, 1, 0, -1]
        self.transform_matrix = []
        self.length = 0

    def gen_pattern_row(self, element_idx):
        pattern = []
        for val in self.base_pattern:
            pattern = np.append(pattern, list(itertools.repeat(val, element_idx + 1)))
        pattern = np.resize(pattern, self.length + 1)
        pattern = np.roll(pattern, -1)
        return np.resize(pattern, self.length)

    def create_transform_matrix(self):
        pattern = []
        for idx in range(self.length):
            pattern = np.append(pattern, self.gen_pattern_row(idx))
        self.transform_matrix = np.reshape(pattern, [self.length, self.length])

    def run_phase(self, split_signal):
        mult = split_signal * self.transform_matrix
        sums = np.sum(mult, 1)
        digits = abs(sums) % 10
        return digits

    def run(self, input_signal, phases):
        self.length = len(input_signal)
        self.create_transform_matrix()
        split_signal = np.array(list(map(int, [char for char in input_signal])))
        for phase in range(phases):
            split_signal = self.run_phase(split_signal)
        return ''.join(map(lambda x: str(int(x)), split_signal))


def test_phases():
    fft = FFT()
    assert fft.run('12345678', 1) == '48226158'

    assert fft.run('12345678', 4) == '01029498'
    assert fft.run('80871224585914546619083218645595', 100)[:8] == '24176176'
    assert fft.run('19617804207202209144916044189917', 100)[:8] == '73745418'
    assert fft.run('69317163492948606335995924319873', 100)[:8] == '52432133'

test_phases()



def run_first_part():
    fft = FFT()
    return fft.run(data, 100)[:8]
print(f"16a: {run_first_part()}")


def find_message(input_str, multiple=10000, phase_count=100):
    # fft = FFT()
    # input_signal = ''.join(itertools.repeat(input_str, multiple))
    # output = fft.run(input_signal, phase_count)
    # # First 8 digits are offset
    # offset = int(input_str[:8])
    # message = output[offset:offset + 8]
    # return message
    offset = int(input_str[:7])
    digits = [int(i) for i in input_str]
    # If `rep` is `digits` repeated 10K times, construct:
    #     arr = [rep[-1], rep[-2], ..., rep[offset]]
    l = multiple * len(digits) - offset
    i = cycle(reversed(digits))
    arr = [next(i) for _ in range(l)]
    # Repeatedly take the partial sums mod 10
    for _ in range(phase_count):
        arr = [n % 10 for n in accumulate(arr)]
    return "".join(str(i) for i in arr[-1:-9:-1])

def test_message_finding():
    assert find_message('03036732577212944063491565474664') == '84462026'
    assert find_message('02935109699940807407585447034323') == '78725270'
    assert find_message('03081770884921959731165446850517') == '53553731'
test_message_finding()

print(f"16b: {find_message(data)}")

