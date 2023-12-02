from aocd import data
import re
from heapq import heappush, heappop


# game state is a big old tuple:
# (boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns)
def start_state():
    return base_boss[0], base_player[0], base_player[1], 0, 0, 0


# end state is any where the first item of the tuple is zero.

spell_mana = {'Magic Missile': 53, 'Drain': 73, 'Shield': 113, 'Poison': 173, 'Recharge': 229}


def cast_possible_spells(dist_and_state):
    dist, state = dist_and_state
    next_states = []
    if state[1] <= 0 or state[0] <= 0:
        # No moves available from this state.
        return next_states
    for s, mana in spell_mana.items():
        if state[2] < mana:
            continue
        if s == 'Shield' and state[3] > 0:
            continue
        if s == 'Poison' and state[4] > 0:
            continue
        if s == 'Recharge' and state[5] > 0:
            continue
        new_state = cast_spell(state, s)
        if new_state[1] > 0 or new_state[0] <= 0:
            next_states.append((dist + mana, new_state))
    return next_states


def apply_effects(state):
    boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns = state
    if poison_turns > 0:
        boss_hp -= 3
    if recharge_turns > 0:
        mana += 101
    shield_turns = max(shield_turns - 1, 0)
    poison_turns = max(poison_turns - 1, 0)
    recharge_turns = max(recharge_turns - 1, 0)
    return boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns


def cast_spell(state, spell_name):
    boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns = state
    # Cast spell
    mana -= spell_mana[spell_name]
    if spell_name == 'Magic Missile':
        boss_hp -= 4
    elif spell_name == 'Drain':
        boss_hp -= 2
        player_hp += 2
    elif spell_name == 'Shield':
        shield_turns = 6
    elif spell_name == 'Poison':
        poison_turns = 6
    elif spell_name == 'Recharge':
        recharge_turns = 5

    if boss_hp > 0:
        state = (boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns)
        boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns = apply_effects(state)

        # process counter attack
        armor = 0 if shield_turns == 0 else 7
        damage = max(base_boss[1] - armor, 1)
        player_hp -= damage

    return boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns

def lose_hp(state):
    boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns = state
    player_hp -= 1
    return boss_hp, player_hp, mana, shield_turns, poison_turns, recharge_turns

def lowest_mana_cost(part=1):
    visited = set()
    pending = []
    heappush(pending, (0, start_state()))
    while pending:
        dist, state = heappop(pending)
        if part == 2:
            state = lose_hp(state)
            if state[1] <= 0:
                continue
        state = apply_effects(state)
        if state[0] <= 0:
            return dist
        if state[1] <= 0:
            continue
        if state in visited:
            # We've been in this same state before, so skip.
            continue
        next_states = cast_possible_spells((dist, state))
        for x in next_states:
            heappush(pending, x)
        visited.add(state)
    raise RuntimeError('Did not reach end goal')


base_player = (10, 250)
base_boss = (13, 8)
assert lowest_mana_cost() == 226

base_player = (10, 250)
base_boss = (14, 8)
assert lowest_mana_cost() == 641

base_boss = (int(re.search(r'Hit Points: (\d+)', data).group(1)),
             int(re.search(r'Damage: (\d+)', data).group(1)))
base_player = (50, 500)
print(f'22a: {lowest_mana_cost()}')

print(f'22b: {lowest_mana_cost(part=2)}')
