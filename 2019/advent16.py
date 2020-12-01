import numpy as np
import itertools


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

input = '59755896917240436883590128801944128314960209697748772345812613779993681653921392130717892227131006192013685880745266526841332344702777305618883690373009336723473576156891364433286347884341961199051928996407043083548530093856815242033836083385939123450194798886212218010265373470007419214532232070451413688761272161702869979111131739824016812416524959294631126604590525290614379571194343492489744116326306020911208862544356883420805148475867290136336455908593094711599372850605375386612760951870928631855149794159903638892258493374678363533942710253713596745816693277358122032544598918296670821584532099850685820371134731741105889842092969953797293495'


def run_first_part():
    fft = FFT()
    return fft.run(input, 100)[:8]


print(f"16a: {run_first_part()}")


def find_message(input_str, multiple=10000, phase_count=100):
    fft = FFT()
    input_signal = ''.join(itertools.repeat(input_str, multiple))
    output = fft.run(input_signal, phase_count)
    # First 8 digits are offset
    offset = int(input_str[:8])
    message = output[offset:offset + 8]
    return message


def test_message_finding():
    assert find_message('03036732577212944063491565474664') == '84462026'
    assert find_message('02935109699940807407585447034323') == '78725270'
    assert find_message('03081770884921959731165446850517') == '53553731'


test_message_finding()
