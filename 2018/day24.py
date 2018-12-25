from functools import partial
from operator import attrgetter
import copy
import re

# Part 1


class Group():
    def __init__(self, units, hp, weaknesses, immunities, attack, attack_type,
                 initiative):
        self.units = units
        self.hp = hp
        self.weaknesses = frozenset(weaknesses)
        self.immunities = frozenset(immunities)
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.units == other.units and self.hp == other.hp and self.weaknesses == other.weaknesses and self.immunities == other.immunities and self.attack == other.attack and self.attack_type == other.attack_type and self.initiative == other.initiative
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'Group(units={}, hp={}, weaknesses={}, immunities={}, attack={}, attack_type={}, initiative={})'.format(self.units, self.hp, self.weaknesses, self.immunities, self.attack, self.attack_type, self.initiative)


def parse_line(s):
    units, hp, attack, initiative = map(int, re.findall(r'\d+', s))
    weakness_idx_match = re.search(r'weak to', s)
    if weakness_idx_match:
        weakness_idx = weakness_idx_match.end()
        weakness_end_idx = re.search(r';|\)', s[weakness_idx:]).start() + weakness_idx
        weaknesses = [e for _, e in re.findall(r'((?:, )?(\w+))', s[weakness_idx:weakness_end_idx])]
    else:
        weaknesses = []
    immunities_idx_match = re.search(r'immune to', s)
    if immunities_idx_match:
        immunities_idx = immunities_idx_match.end()
        immunities_end_idx = re.search(r';|\)', s[immunities_idx:]).start() + immunities_idx
        immunities = [e for _, e in re.findall(r'((?:, )?(\w+))', s[immunities_idx:immunities_end_idx])]
    else:
        immunities = []
    attack_type = re.findall(r'(\w+) (?=damage)', s)[0]
    return Group(units, hp, weaknesses, immunities, attack, attack_type,
                 initiative)


def parse_input(fname):
    with open(fname) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    infection_idx = lines.index('Infection:')
    immunity_groups = [parse_line(l) for l in lines[1:infection_idx]]
    infection_groups = [parse_line(l) for l in lines[infection_idx + 1:]]
    return immunity_groups, infection_groups


def effective_power(group):
    return group.units * group.attack


def sort_for_selection(groups):
    gs = sorted(groups, key=attrgetter('initiative'), reverse=True)
    gs.sort(key=effective_power, reverse=True)
    return gs


def calculate_damage(group, enemy_group):
    mult = 1
    if group.attack_type in enemy_group.immunities:
        mult = 0
    elif group.attack_type in enemy_group.weaknesses:
        mult = 2
    return effective_power(group) * mult


def sort_by_damage(group, enemy_groups):
    gs = sorted(enemy_groups, key=attrgetter('initiative'), reverse=True)
    gs.sort(key=effective_power, reverse=True)
    gs.sort(key=partial(calculate_damage, group), reverse=True)
    return gs


def select_target(group, enemy_groups):
    if not enemy_groups:
        return None
    enemy_group = sort_by_damage(group, enemy_groups)[0]
    return enemy_group if calculate_damage(group, enemy_group) > 0 else None


def units_killed(group, enemy_group):
    return calculate_damage(group, enemy_group) / enemy_group.hp


def fight(immunity_groups, infection_groups):
    immunity_groups = copy.deepcopy(immunity_groups)
    infection_groups = copy.deepcopy(infection_groups)
    imgs = immunity_groups[:]
    ings = infection_groups[:]
    pairs = []
    for g in sort_for_selection(immunity_groups):
        enemy = select_target(g, ings)
        if enemy:
            pairs.append((g, enemy))
            ings.remove(enemy)
    for g in sort_for_selection(infection_groups):
        enemy = select_target(g, imgs)
        if enemy:
            pairs.append((g, enemy))
            imgs.remove(enemy)
    for g, enemy in sorted(pairs, key=lambda (g, _): g.initiative, reverse=True):
        if g.units <= 0:
            continue
        enemy.units -= units_killed(g, enemy)
    return filter(lambda g: g.units > 0, immunity_groups), filter(lambda g: g.units > 0, infection_groups)


def combat(immunity_groups, infection_groups):
    while immunity_groups and infection_groups:
        immunity_groups, infection_groups = fight(immunity_groups,
                                                  infection_groups)
    return sum(map(attrgetter('units'), immunity_groups or infection_groups))

# Part 2


def immunity_wins(immunity_groups, infection_groups):
    prev_imgs = prev_ings = None
    stall = False
    while immunity_groups and infection_groups:
        immunity_groups, infection_groups = fight(immunity_groups,
                                                  infection_groups)
        if prev_imgs == immunity_groups and prev_ings == infection_groups:
            stall = True
            break
        prev_imgs = immunity_groups
        prev_ings = infection_groups
    return not stall and len(immunity_groups) > 0, immunity_groups, infection_groups


def smallest_boost_units(immunity_groups, infection_groups):
    win = False
    imgs = copy.deepcopy(immunity_groups)
    while not win:
        for g in imgs:
            g.attack += 1
        win, win_imgs, _ = immunity_wins(imgs, infection_groups)
    return sum(map(attrgetter('units'), win_imgs))


if __name__ == '__main__':
    immunity_groups, infection_groups = parse_input('./resources/day24.txt')
    print('Part 1: {}'.format(combat(immunity_groups, infection_groups)))
    print('Part 2: {}'.format(smallest_boost_units(immunity_groups, infection_groups)))
