from aocd import data
from collections import defaultdict
from functools import reduce

def run(data, part=1):
    bids = {}
    for line in data.splitlines():
        (hand, bid) = line.split()
        bids[hand] = int(bid)
    
    ranked_hands = sorted(bids.keys(), key=lambda x: hand_value(x, part))
    winnings = [(1+idx)*bids[hand] for (idx,hand) in enumerate(ranked_hands)]
    return sum(winnings)

def hand_value(hand, part=1):
    all_cards = '23456789TJQKA' if part == 1 else 'J23456789TQKA'
    card_vals = [all_cards.find(x) for x in hand]
    return hand_level(hand, part) + reduce(lambda x,y: 13 * x + y, card_vals)

def hand_level(hand, part=1):
    card_cnts = defaultdict(int)
    cnt_cards = defaultdict(set)
    for c in hand:
        card_cnts[c] += 1
    for (card,cnt) in card_cnts.items():
        cnt_cards[cnt].add(card)
    
    if part > 1:
        # turns Js into whatever has the most
        num_js = card_cnts['J']
        if num_js > 0 and num_js < 5:
            del card_cnts['J']
            high_bucket = sorted(cnt_cards.keys())[-1]
            card_cnts[next(iter(cnt_cards[high_bucket]))] += num_js
            # redo cnt_cards
            cnt_cards.clear()
            for (card,cnt) in card_cnts.items():
                cnt_cards[cnt].add(card)
    
    if 5 in cnt_cards:
        # five of a kind
        return 6000000
    if 4 in cnt_cards:
        # four of a kind
        return 5000000
    if 3 in cnt_cards and 2 in cnt_cards:
        # full house
        return 4000000
    if 3 in cnt_cards:
        # three of a kind
        return 3000000
    if 2 in cnt_cards:
        if len(cnt_cards[2]) == 2:
            # two pair
            return 2000000
        # one pair
        return 1000000
    # high card
    return 0


ex1='''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''

assert run(ex1) == 6440
print('7a: ', run(data))
assert run(ex1, part=2) == 5905
print('7b: ', run(data, part=2))