from aocd import numbers

def count_window_increases(measurements, window_size = 3):
    count = 0
    for idx in range(window_size, len(measurements)):
        if measurements[idx] > measurements[idx - window_size]:
            count += 1
    return count 

def count_increases(measurements):
    return count_window_increases(measurements, 1)

assert count_increases([199,200,208,210,200,207,240,269,260,263]) == 7
print('1a: ', count_increases(numbers))


assert count_window_increases([199,200,208,210,200,207,240,269,260,263]) == 5
print('1b: ', count_window_increases(numbers))