from aocd import data 

def play_bingo(input, first_win = True):
    (calls, cards) = parse_input(input)
    for call in calls:
        mark_cards(call, cards)
        matching_indices = []
        for idx, card in enumerate(cards):
            if bingo_found(card):
                if first_win:
                    return call * score_card(card)
                # When not using the first win, we remove the bingo'd card until it's the last one.
                if len(cards) == 1:
                    return call * score_card(card)
                matching_indices.append(idx)
        if not first_win and matching_indices:
            for idx in matching_indices[::-1]:
                cards = cards[:idx] + cards[idx + 1:]

def parse_input(input_data):
    first_line = input_data.splitlines()[0]
    calls = [int(n) for n in first_line.split(',')]

    cards = []
    card_inputs = input_data.split("\n\n")[1:]
    for card_input in card_inputs:
        card = []
        for line in card_input.splitlines():
            card.append([])
            for val in line.split():
                card[-1].append(int(val))
        cards.append(card)
    return (calls, cards)

def mark_cards(call, cards):
    for card in cards:
        for row in range(0, len(card)):
            for col in range(0, len(card[row])):
                if card[row][col] == call:
                    card[row][col] = -1

def bingo_found(card):
    for row in card:
        if sum(row) == -1 * len(row):
            return True
    for col in range(0, len(card)):
        total = 0
        for row in range(0, len(card)):
            total += card[row][col]
        if total == -1 * len(card):
            return True
    return False

def score_card(card):
    sum = 0
    for row in card:
        for col in row:
            if col != -1:
                sum += col
    return sum

test="""7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

assert play_bingo(test) == 4512
print('4a: ', play_bingo(data))

assert play_bingo(test, False) == 1924
print('4b: ', play_bingo(data, False))

