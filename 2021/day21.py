from aocd import lines
from functools import lru_cache

def roll():
    next_roll = 1
    while True:
        yield next_roll
        next_roll = next_roll + 1
        if next_roll > 100:
            next_roll = 1

class Game:
    def __init__(self, inputlines):
        self.players = [ int(inputlines[0][-2:]), int(inputlines[1][-2:]) ]
        self.scores = [0, 0]
        self.times_rolled = 0
        self.cur_die = 1

    def roll_die(self):
        self.times_rolled += 1
        ret = self.cur_die 
        self.cur_die += 1
        if self.cur_die > 100:
            self.cur_die = 1
        return ret

    def play(self):
        cur_player = 0
        while True:
            roll = self.roll_die() + self.roll_die() + self.roll_die()
            self.players[cur_player] = (self.players[cur_player] + roll) % 10 or 10
            self.scores[cur_player] += self.players[cur_player]
            if self.scores[cur_player] >= 1000:
                return self.times_rolled * self.scores[(cur_player + 1) % 2]
            cur_player = (cur_player + 1) % 2


test = """Player 1 starting position: 4
Player 2 starting position: 8
"""
assert Game(test.splitlines()).play() == 739785
print('21a: ', Game(lines).play())

three_rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
class Game2: 
    def __init__(self, inputlines):
        self.starting_pos = [ int(inputlines[0][-2:]), int(inputlines[1][-2:]) ]
        # states are cur_loc[0], cur_loc[1], score[0], score[1], and the current player.
        # self.state_counts = {(starting_pos[0], starting_pos[1], 0, 0, 0): 1}

    @lru_cache(maxsize=None)
    def evolve_state(self, pos0, pos1, score0, score1, player):
        if score0 >= self.to_win:
            return (1, 0)
        if score1 >= self.to_win:
            return (0, 1)
        num_wins = (0,0)
        for roll1 in range(1,4):
            for roll2 in range(1,4):
                for roll3 in range(1,4):
                    roll = roll1 + roll2 + roll3
                    if player == 0:
                        position = (pos0 + roll) % 10 or 10
                        total = score0 + position
                        (win0, win1) = self.evolve_state(position, pos1, total, score1, 1)
                    else:
                        position = (pos1 + roll) % 10 or 10
                        total = score1 + position
                        (win0, win1) = self.evolve_state(pos0, position, score0, total, 0)
                    num_wins = (num_wins[0] + win0, num_wins[1] + win1)
        return num_wins

    def play(self, to_win=21):
        self.to_win = to_win
        return self.evolve_state(self.starting_pos[0], self.starting_pos[1], 0, 0, 0)

    # def play(self, to_win=21):
    #     pos = [0,0]
    #     score = [0,0]
    #     while len(self.state_counts):
    #         (state, state_cnt) = next(iter(self.state_counts.items()))
    #         del self.state_counts[state]
    #         (pos[0], pos[1], score[0], score[1], player) = state
    #         for (roll, roll_cnt) in three_rolls.items():
    #             position = (pos[player] + roll) % 10 or 10
    #             total = score[player] + position
    #             if total >= to_win:
    #                 self.player_wins[player] += (state_cnt * roll_cnt)
    #                 continue                    
    #             if player == 0:
    #                 new_state = (position, pos[1], total, score[1], 1)
    #             else:
    #                 new_state = (pos[0], position, score[0], total, 0)
    #             self.state_counts[new_state] = (state_cnt * roll_cnt)
    #     print(f'G2: {self.player_wins}')
    #     return self.player_wins

assert max(Game2(test.splitlines()).play()) == 444356092776315
print('21b: ', max(Game2(lines).play()))
