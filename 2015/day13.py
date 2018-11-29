import re
import itertools

# Part 1


def parse_instruction(s):
    x, op, n, y = re.match(
        '(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).',
        s).groups()
    return (x, y, -int(n) if op == 'lose' else int(n))


def parse_instructions(ss):
    return [parse_instruction(s) for s in ss]


def distance_map(instructions):
    m = {}
    for x, y, n in instructions:
        if m.get((y, x)):
            m[(x, y)] = m[(y, x)] = m[(y, x)] + n
        else:
            m[(x, y)] = n
    return m


def persons(m):
    ps = set()
    for (x, y) in m:
        ps.add(x)
        ps.add(y)
    return sorted(list(ps))


def max_happiness(distance_m):
    ps = persons(distance_m)
    n = len(ps)
    P = frozenset(ps[1:])
    C = {}

    for p in P:
        C[(frozenset([p]), p)] = distance_m[(ps[0], p)]

    for k in range(2, n):
        for S in (frozenset(c) for c in itertools.combinations(P, k)):
            for s in S:
                S_s = frozenset(S.difference([s]))
                C[(S,
                   s)] = max([C[(S_s, m)] + distance_m[(m, s)] for m in S_s])

    return max([C[(P, m)] + distance_m[(m, ps[0])] for m in P])


# Part 2


def distance_map_self(instructions):
    m = distance_map(instructions)
    for p in persons(m):
        m[('self', p)] = m[(p, 'self')] = 0
    return m


if __name__ == '__main__':
    with open('./resources/day13.txt', 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    instructions = parse_instructions(lines)
    print('Part 1: {}'.format(max_happiness(distance_map(instructions))))
    print('Part 2: {}'.format(max_happiness(distance_map_self(instructions))))
