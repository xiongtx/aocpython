import copy
import heapq
import sys

# Part 1


def unit_map(cave):
    positions = [(i, j) for i in range(len(cave)) for j in range(len(cave[0]))
                 if cave[i][j] in {'E', 'G'}]
    return {(i, j): (cave[i][j], 200) for i, j in positions}


def parse_input(fname):
    with open(fname, 'r') as f:
        cave = [list(l.rstrip()) for l in f.readlines()]
    return cave, unit_map(cave)


def enemy_positions(c, units_m):
    return [pos for pos, (C, _) in units_m.iteritems() if c != C]


def adjacents((i, j)):
    return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]


def open_positions(c, cave, units_m, e_positions):
    return [(i, j) for pos in e_positions for i, j in adjacents(pos)
            if (i, j) not in units_m.keys() and cave[i][j] != '#']


def outcome(rounds, units_m):
    return rounds * sum(hp for (_, hp) in units_m.itervalues())


def next_position(start, ends, cave, units_m):
    min_d = sys.maxint
    paths = []
    unvisited = {(i, j)
                 for i in range(len(cave)) for j in range(len(cave[0]))
                 if (i, j) not in units_m.keys() and cave[i][j] != '#'}
    unvisited_ends = set(ends)
    pq = [(0, start, [])]

    while pq and unvisited_ends:
        d, pos, path = heapq.heappop(pq)
        if d > min_d:
            continue
        if pos in unvisited_ends:
            paths.append(path)
            min_d = d
            unvisited_ends.remove(pos)
        for adj in filter(lambda p: p in unvisited, adjacents(pos)):
            heapq.heappush(pq, (d + 1, adj, path + [adj]))
            unvisited.remove(adj)
    return sorted(filter(lambda path: len(path) == min_d,
                         paths))[0][0] if paths else None


def in_range(pos, e_positions):
    return pos in [adj for e_pos in e_positions for adj in adjacents(e_pos)]


def next_enemy(pos, e_positions, units_m):
    adj_enemies = filter(lambda e_pos: e_pos in adjacents(pos), e_positions)
    return sorted([(hp, p) for p, (_, hp) in units_m.iteritems()
                   if p in adj_enemies])[0][1] if adj_enemies else None


def play(cave, units_m):
    attack_power = 3
    rounds = 0
    while True:
        for pos, (c, hp) in sorted(units_m.items()):
            if pos in units_m.keys():
                units_m = copy.copy(units_m)
                e_positions = enemy_positions(c, units_m)
                if not e_positions:
                    return outcome(rounds, units_m)
                if not in_range(pos, e_positions):
                    o_positions = open_positions(c, cave, units_m, e_positions)
                    if not o_positions:
                        continue
                    next_pos = next_position(pos, o_positions, cave, units_m)
                    if not next_pos:
                        continue
                    units_m[next_pos] = units_m[pos]
                    del units_m[pos]
                else:
                    next_pos = pos
                next_e = next_enemy(next_pos, e_positions, units_m)
                if next_e:
                    e, e_hp = units_m[next_e]
                    if e_hp - attack_power <= 0:
                        del units_m[next_e]
                    else:
                        units_m[next_e] = (e, e_hp - attack_power)
        rounds += 1


# Part 2


def play_no_losses(cave, units_m, elf_attack):
    goblin_attack = 3
    rounds = 0
    while True:
        for pos, (c, hp) in sorted(units_m.items()):
            if pos in units_m.keys():
                units_m = copy.copy(units_m)
                e_positions = enemy_positions(c, units_m)
                if not e_positions:
                    return outcome(rounds, units_m)
                if not in_range(pos, e_positions):
                    o_positions = open_positions(c, cave, units_m, e_positions)
                    if not o_positions:
                        continue
                    next_pos = next_position(pos, o_positions, cave, units_m)
                    if not next_pos:
                        continue
                    units_m[next_pos] = units_m[pos]
                    del units_m[pos]
                else:
                    next_pos = pos
                next_e = next_enemy(next_pos, e_positions, units_m)
                if next_e:
                    e, e_hp = units_m[next_e]
                    if e == 'G':
                        if e_hp - elf_attack <= 0:
                            del units_m[next_e]
                        else:
                            units_m[next_e] = (e, e_hp - elf_attack)
                    else:
                        if e_hp - goblin_attack <= 0:
                            return None
                        else:
                            units_m[next_e] = (e, e_hp - goblin_attack)
        rounds += 1


def play_until_no_losses(cave, units_m):
    elf_attack = 3
    while True:
        result = play_no_losses(cave, units_m, elf_attack)
        if result:
            return result
        else:
            elf_attack += 1


if __name__ == '__main__':
    cave, units_m = parse_input('./resources/day15.txt')
    print('Part 1: {}'.format(play(cave, units_m)))
    print('Part 2: {}'.format(play_until_no_losses(cave, units_m)))
