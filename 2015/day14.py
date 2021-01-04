from aocd import data
import re
from collections import defaultdict


class ReindeerOlympics:
    def __init__(self):
        self.reindeer = {}

    def add_reindeer(self, input_str):
        for line in input_str.splitlines():
            reindeer, speed, duration, rest = re.match(
                r'(\w+) can fly (\d+) km/s for (\d+) seconds.*rest for (\d+) seconds', line).groups()
            self.reindeer[reindeer] = (int(speed), int(duration), int(rest))
        return self

    def dist(self, reindeer, time):
        speed, duration, rest = self.reindeer[reindeer]
        mults = time // (duration + rest)
        rem = time % (duration + rest)
        return speed * duration * mults + (speed * min(duration, rem))

    def best_deer(self, time):
        best_deer = []
        max_score = 0
        for d in self.reindeer.keys():
            score = self.dist(d, time)
            if score > max_score:
                max_score, best_deer = score, [d]
            elif score == max_score:
                best_deer.append(d)
        return best_deer, max_score

    def cum_points(self, end_time):
        # Slow version
        scores = defaultdict(int)
        for t in range(1, end_time + 1):
            best_deer_list, _ = self.best_deer(t)
            for d in best_deer_list:
                scores[d] = scores[d] + 1
        return max(scores.values())


test_input = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''
assert ReindeerOlympics().add_reindeer(test_input).best_deer(1000) == (['Comet'], 1120)
print('14a: ', ReindeerOlympics().add_reindeer(data).best_deer(2503))

assert ReindeerOlympics().add_reindeer(test_input).cum_points(1000) == 689
print('14b: ', ReindeerOlympics().add_reindeer(data).cum_points(2503))
