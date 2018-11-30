import re

# Part 1


def parse_input(s):
    x, s, t, r = re.match(
        '(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.',
        s).groups()
    return (x, int(s), int(t), int(r))


def parse_inputs(ss):
    return [parse_input(s) for s in ss]


def distance((_, s, t, r), T):
    n, left = divmod(T, t + r)
    return s * (n * t + min(t, left))


def winning_distance(all_deer, T):
    return max(distance(deer, T) for deer in all_deer)


# Part 2


def winning_points(all_deer, T):
    distance_m = {x: 0 for (x, _, _, _) in all_deer}
    points_m = distance_m.copy()
    for i in range(T):
        for x, s, t, r in all_deer:
            distance_m[x] += s if (i % (t + r)) < t else 0
        max_d = max(distance_m.itervalues())
        for x in (k for k, v in distance_m.iteritems() if v == max_d):
            points_m[x] += 1
    return max(points_m.itervalues())


if __name__ == '__main__':
    with open('./resources/day14.txt', 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    all_deer = parse_inputs(lines)
    print('Part 1: {}'.format(winning_distance(all_deer, 2503)))
    print('Part 2: {}'.format(winning_points(all_deer, 2503)))
