from collections import namedtuple
import copy
import heapq

boss = {'Hit Points': 71, 'Damage': 10}
player = {'Hit Points': 50, 'Mana': 500, 'Effects': {}, 'Cast spells': []}

Spell = namedtuple(
    'Spell', ['name', 'cost', 'turns', 'damage', 'armor', 'heal', 'mana_heal'])
Spell.__new__.__defaults__ = (None, ) + (0, ) * (len(Spell._fields) - 1)

spells = {
    'Magic Missile': Spell(name='Magic Missile', cost=53, turns=0, damage=4),
    'Drain': Spell(name='Drain', cost=73, turns=0, damage=2, heal=2),
    'Shield': Spell(name='Shield', cost=113, turns=6, armor=7),
    'Poison': Spell(name='Poison', cost=173, turns=6, damage=3),
    'Recharge': Spell(name='Recharge', cost=229, turns=5, mana_heal=101)
}


def cast_spell(player, boss, spell):
    player = copy.deepcopy(player)
    boss = copy.deepcopy(boss)

    player['Mana'] -= spell.cost
    player['Cast spells'].append(spell.name)
    if spell.turns == 0:
        boss['Hit Points'] -= spell.damage
        player['Hit Points'] += spell.heal
    else:
        player['Effects'][spell.name] = spell.turns

    return player, boss


def apply_effects(player, boss):
    player = copy.deepcopy(player)
    boss = copy.deepcopy(boss)
    for name in player['Effects']:
        if name == 'Shield':
            player['Armor'] = spells[name].armor
        elif name == 'Poison':
            boss['Hit Points'] -= spells[name].damage
        elif name == 'Recharge':
            player['Mana'] += spells[name].mana_heal
        player['Effects'][name] -= 1
    return player, boss


def cleanup_effects(player):
    player = copy.deepcopy(player)
    if 'Shield' in player['Effects'] and player['Effects']['Shield'] == 0:
        del player['Armor']
    player['Effects'] = {
        name: turns
        for name, turns in player['Effects'].iteritems() if turns > 0
    }
    return player


def next_states(player, boss, whose):
    player, boss = apply_effects(player, boss)

    if boss['Hit Points'] <= 0:
        return [(0, player, boss)]

    states = []
    if whose == 'Player':
        excluded_names = [k for k, v in player['Effects'].iteritems() if v > 0]
        available_spells = [
            spell for name, spell in spells.iteritems()
            if name not in excluded_names and player['Mana'] >= spell.cost
        ]

        if not available_spells:
            player['Hit Points'] = 0
            return [(0, player, boss)]

        for spell in available_spells:
            p, b = cast_spell(player, boss, spell)
            states.append((spell.cost, cleanup_effects(p), b))
    else:
        p = copy.deepcopy(player)
        p['Hit Points'] -= max(boss['Damage'] - p.get('Armor', 0), 1)
        states.append((0, cleanup_effects(p), boss))
    return states


def min_mana_win(player, boss):
    pq = [(0, player, boss, 'Player')]
    while pq:
        mana_spent, player, boss, whose = heapq.heappop(pq)

        if boss['Hit Points'] <= 0:
            return mana_spent

        if player['Hit Points'] <= 0:
            continue

        for mana, p, b in next_states(player, boss, whose):
            w = 'Player' if whose != 'Player' else 'Boss'
            heapq.heappush(pq, (mana_spent + mana, p, b, w))


# Part 2


def next_states_hard(player, boss, whose):
    # Auto lose 1 HP at start of each turn
    player = copy.deepcopy(player)
    if whose == 'Player':
        player['Hit Points'] -= 1
    if player['Hit Points'] <= 0:
        return [(0, player, boss)]

    player, boss = apply_effects(player, boss)
    if boss['Hit Points'] <= 0:
        return [(0, player, boss)]

    states = []
    if whose == 'Player':
        excluded_names = [k for k, v in player['Effects'].iteritems() if v > 0]
        available_spells = [
            spell for name, spell in spells.iteritems()
            if name not in excluded_names and player['Mana'] >= spell.cost
        ]

        if not available_spells:
            player['Hit Points'] = 0
            return [(0, player, boss)]

        for spell in available_spells:
            p, b = cast_spell(player, boss, spell)
            states.append((spell.cost, cleanup_effects(p), b))
    else:
        p = copy.deepcopy(player)
        p['Hit Points'] -= max(boss['Damage'] - p.get('Armor', 0), 1)
        states.append((0, cleanup_effects(p), boss))
    return states


def min_mana_win_hard(player, boss):
    pq = [(0, player, boss, 'Player')]
    while pq:
        mana_spent, player, boss, whose = heapq.heappop(pq)

        if boss['Hit Points'] <= 0:
            return mana_spent

        if player['Hit Points'] <= 0:
            continue

        for mana, p, b in next_states_hard(player, boss, whose):
            w = 'Player' if whose != 'Player' else 'Boss'
            heapq.heappush(pq, (mana_spent + mana, p, b, w))


if __name__ == '__main__':
    print('Part 1: {}'.format(min_mana_win(player, boss)))
    print('Part 2: {}'.format(min_mana_win_hard(player, boss)))
