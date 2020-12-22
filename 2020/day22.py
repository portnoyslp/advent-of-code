from aocd import data

games_of_combat = 0

class Combat:
    def __init__(self):
        self.decks = ([], [])
        self.deck_history = set()

    @classmethod
    def from_string(cls, starting_decks):
        combat = cls()
        (player1, player2) = starting_decks.split('\n\n')
        for line in player1.splitlines():
            if 'Player' in line:
                continue
            combat.decks[0].append(int(line))
        for line in player2.splitlines():
            if 'Player' in line:
                continue
            combat.decks[1].append(int(line))
        return combat

    @classmethod
    def from_decks(cls, decks):
        combat = cls()
        combat.decks = decks
        return combat

    def play_round(self):
        p1 = self.decks[0].pop(0)
        p2 = self.decks[1].pop(0)
        if p1 > p2:
            self.decks[0].extend([p1, p2])
        else:
            self.decks[1].extend([p2, p1])

    def score(self, winner):
        deck = self.decks[winner]
        scores = range(len(deck), 0, -1)
        return winner + 1, sum(map(lambda x: x[0] * x[1], zip(deck, scores)))

    def play(self):
        while len(self.decks[0]) > 0 and len(self.decks[1]) > 0:
            self.play_round()
        winner = 0 if len(self.decks[0]) > 0 else 1
        return self.score(winner)

    def recursive_round(self):
        p1 = self.decks[0].pop(0)
        p2 = self.decks[1].pop(0)
        winner = p2 > p1
        if len(self.decks[0]) >= p1 and len(self.decks[1]) >= p2:
            decks = (self.decks[0][:p1], self.decks[1][:p2])
            winner, _ = Combat().from_decks(decks).recursive_combat()
            winner -= 1
        self.decks[winner].extend([p1, p2] if winner == 0 else [p2, p1])

    def recursive_combat(self):
        global games_of_combat
        games_of_combat += 1
        print(f"Recursive Combat game {games_of_combat}")
        while len(self.decks[0]) > 0 and len(self.decks[1]) > 0:
            state = (tuple(self.decks[0]), tuple(self.decks[1]))
            if state in self.deck_history:
                return self.score(0)
            self.deck_history.add(state)
            self.recursive_round()
        winner = 0 if len(self.decks[0]) > 0 else 1
        return self.score(winner)


test_input = '''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10'''
assert Combat().from_string(test_input).play() == (2, 306)
print('22a: ', Combat().from_string(data).play())

assert Combat().from_string(test_input).recursive_combat() == (2, 291)
print('22b: ', Combat().from_string(data).recursive_combat())
