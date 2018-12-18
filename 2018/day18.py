from collections import defaultdict
from itertools import chain
import copy


def adjacents((i, j), max_x, max_y):
    return [(x, y) for x in range(i - 1, i + 2) for y in range(j - 1, j + 2)
            if (x, y) != (i, j) and 0 <= x < max_x and 0 <= y < max_y]


def parse_input(fname):
    with open(fname) as f:
        grid = [list(l.rstrip()) for l in f.readlines()]
    return grid


def evolve(grid, t):
    max_x = len(grid)
    max_y = len(grid[0])
    for t in range(t):
        new_grid = copy.deepcopy(grid)
        for i in range(max_x):
            for j in range(max_y):
                adjs = adjacents((i, j), max_x, max_y)
                if grid[i][j] == '.':
                    if sum(grid[x][y] == '|' for x, y in adjs) >= 3:
                        new_grid[i][j] = '|'
                elif grid[i][j] == '|':
                    if sum(grid[x][y] == '#' for x, y in adjs) >= 3:
                        new_grid[i][j] = '#'
                elif grid[i][j] == '#':
                    if not (sum(grid[x][y] == '#' for x, y in adjs) >= 1
                            and sum(grid[x][y] == '|' for x, y in adjs) >= 1):
                        new_grid[i][j] = '.'
        grid = new_grid
    n_lumb = sum(c == '#' for c in chain(*grid))
    n_tree = sum(c == '|' for c in chain(*grid))
    return grid, n_lumb * n_tree


def evenly_spaced(l):
    x = l[1] - l[0]
    for i in range(2, len(l)):
        if l[i] - l[i - 1] != x:
            return False
    return True


def period(grid):
    m = defaultdict(list)
    t = 0
    while True:
        t += 1
        grid, total = evolve(grid, 1)
        if total in m and len(m[total]) >= 3 and evenly_spaced(m[total][-3:]):
            times = m[total]
            return times[-3], times[-1] - times[-2]
        m[total].append(t)


if __name__ == '__main__':
    grid = parse_input('./resources/day18.txt')
    _, total = evolve(grid, 10)
    print('Part 1: {}'.format(total))

    start, p = period(grid)
    _, large_total = evolve(grid, start + (1000000000 - start) % p)
    print('Part 2: {}'.format(large_total))
