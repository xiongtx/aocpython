from functools import partial
from itertools import chain, combinations
import math

weapons = {
    'Dagger': (8, 4, 0),
    'Shortsword': (10, 5, 0),
    'Warhammer': (25, 6, 0),
    'Longsword': (40, 7, 0),
    'Greataxe': (74, 8, 0)
}

armors = {
    'Leather': (13, 0, 1),
    'Chainmail': (31, 0, 2),
    'Splintmail': (53, 0, 3),
    'Bandedmail': (75, 0, 4),
    'Platemail': (102, 0, 5)
}

rings = {
    'Damage +1': (25, 1, 0),
    'Damage +2': (50, 2, 0),
    'Damage +3': (100, 3, 0),
    'Defense +1': (20, 0, 1),
    'Defense +2': (40, 0, 2),
    'Defense +3': (80, 0, 3)
}

boss = {'Hit Points': 104, 'Damage': 8, 'Armor': 1}


def player_wins(player, boss):
    keys = ('Hit Points', 'Damage', 'Armor')
    player_hp, player_damage, player_armor = [player[k] for k in keys]
    boss_hp, boss_damage, boss_armor = [boss[k] for k in keys]

    player_net_damage = max(player_damage - boss_armor, 1)
    boss_net_damage = max(boss_damage - player_armor, 1)

    kill_boss_turns = math.ceil(float(boss_hp) / player_net_damage)
    kill_player_turns = math.ceil(float(player_hp) / boss_net_damage)

    return kill_boss_turns <= kill_player_turns


def items_cost(items):
    return sum(item[0] for item in items)


def equipment_low(weapons, armors, rings):
    return sorted(([w] + list(worn_armors) + list(worn_rings)
                   for worn_armors in chain(
                       *map(partial(combinations, armors.values()), range(2)))
                   for worn_rings in chain(
                       *map(partial(combinations, rings.values()), range(3)))
                   for w in weapons.values()),
                  key=items_cost)


def min_gold_win(weapons, armors, rings, boss):
    for equip in equipment_low(weapons, armors, rings):
        player = {'Hit Points': 100, 'Damage': 0, 'Armor': 0}
        total_cost = items_cost(equip)
        for _, damage, armor in equip:
            player['Damage'] += damage
            player['Armor'] += armor
        if player_wins(player, boss):
            return total_cost


# Part 2


def equipment_high(weapons, armors, rings):
    return sorted(([w] + list(worn_armors) + list(worn_rings)
                   for worn_armors in chain(
                       *map(partial(combinations, armors.values()), range(2)))
                   for worn_rings in chain(
                       *map(partial(combinations, rings.values()), range(3)))
                   for w in weapons.values()),
                  key=items_cost,
                  reverse=True)


def max_gold_lose(weapons, armors, ring, boss):
    for equip in equipment_high(weapons, armors, rings):
        player = {'Hit Points': 100, 'Damage': 0, 'Armor': 0}
        total_cost = items_cost(equip)
        for _, damage, armor in equip:
            player['Damage'] += damage
            player['Armor'] += armor
        if not player_wins(player, boss):
            return total_cost


if __name__ == '__main__':
    print('Part 1: {}'.format(min_gold_win(weapons, armors, rings, boss)))
    print('Part 2: {}'.format(max_gold_lose(weapons, armors, rings, boss)))
