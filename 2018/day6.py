from collections import defaultdict
from functools import partial
import re


def parse_input(s):
    n1, n2 = re.findall('\d+', s)
    return (int(n1), int(n2))


def manhattan_distance((x1, y1), (x2, y2)):
    return abs(x1 - x2) + abs(y1 - y2)


def min_coord(pos, coords):
    Cs = sorted([(manhattan_distance(pos, coord), coord) for coord in coords],
                key=lambda t: t[0])
    min_d, min_coord = Cs[0]
    if sum(d == min_d for (d, coord) in Cs) == 1:
        return min_coord


def max_area(coords):
    xs = map(lambda t: t[0], coords)
    ys = map(lambda t: t[1], coords)
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs) + 1
    max_y = max(ys) + 1
    grid = [[None] * (max_y - min_y) for _ in range(min_x, max_x)]

    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            grid[i - min_x][j - min_y] = min_coord((i, j), coords)

    S = set(coords)
    for i in [min_x, max_x - 1]:
        for j in range(min_y, max_y):
            S.discard(grid[i - min_x][j - min_y])
    for i in range(min_x, max_x):
        for j in [min_y, max_y - 1]:
            S.discard(grid[i - min_x][j - min_y])

    count_m = defaultdict(lambda: 0)
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            pos = grid[i - min_x][j - min_y]
            if pos in S:
                count_m[pos] += 1

    return max(count_m.values())


def total_distance(pos, coords):
    return sum(map(partial(manhattan_distance, pos), coords))


def safe_area(coords):
    xs = map(lambda t: t[0], coords)
    ys = map(lambda t: t[1], coords)

    return sum(
        total_distance((i, j), coords) < 10000
        for i in range(min(xs),
                       max(xs) + 1) for j in range(min(ys),
                                                   max(ys) + 1))


if __name__ == '__main__':
    with open('./resources/day6.txt', 'r') as f:
        coords = [parse_input(l) for l in f.readlines()]
    print('Part 1: {}'.format(max_area(coords)))
    print('Part 2: {}'.format(safe_area(coords)))
