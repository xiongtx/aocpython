import re
import itertools

# Part 1


def parse_input(s):
    x, y, v = re.match(r'(\w+) to (\w+) = (\d+)', s).groups()
    return (x, y, int(v))


def parse_inputs(ss):
    return [parse_input(s) for s in ss]


def locations(inputs):
    locs = set()
    for x, y, _ in inputs:
        locs.update([x, y])
    return locs


def distance_map(inputs):
    m = {}
    for x, y, v in inputs:
        m[(x, y)] = m[(y, x)] = v
    return m


def cost(path, distance_m):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += distance_m[(path[i], path[i + 1])]
    return total_cost


def min_cost(inputs):
    m = distance_map(inputs)
    return min(
        cost(path, m) for path in itertools.permutations(locations(inputs)))


def max_cost(inputs):
    m = distance_map(inputs)
    return max(
        cost(path, m) for path in itertools.permutations(locations(inputs)))


if __name__ == '__main__':
    with open('./resources/day9.txt', 'r') as f:
        inputs = [parse_input(s.rstrip()) for s in f.readlines()]
    print('Part 1: {}'.format(min_cost(inputs)))
    print('Part 2: {}'.format(max_cost(inputs)))
