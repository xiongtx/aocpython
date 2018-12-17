from collections import deque
from itertools import chain
import copy
import re


def parse_input(fname):
    clay = []
    with open(fname, 'r') as f:
        for l in f.readlines():
            xy1, n1, n2, xy2, n3, n4 = re.match(
                r'(x|y)=(\d+)(?:\.\.)?(\d+)?, (x|y)=(\d+)(?:\.\.)?(\d+)?',
                l.rstrip()).groups()
            clay.append({
                xy1: map(int, (n1, n2 or n1)),
                xy2: map(int, (n3, n4 or n3))
            })
    xs = [x for m in clay for k, xs in m.iteritems() for x in xs if k == 'x']
    ys = [y for m in clay for k, ys in m.iteritems() for y in ys if k == 'y']
    x_start = min(xs) - 1
    y_start = min(ys) - 1
    grid = [['.'] * (max(xs) - min(xs) + 3)
            for _ in range(max(ys) - min(ys) + 3)]
    for m in clay:
        x1, x2 = m['x']
        y1, y2 = m['y']
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                grid[y - y_start][x - x_start] = '#'
    return grid, x_start


def flow(grid, x_start):
    points = deque([(500 - x_start, 0)])
    blockers = {'#', '~'}
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    grid = copy.deepcopy(grid)

    while points:
        x, y = points.popleft()
        while y < max_y and grid[y + 1][x] not in blockers:
            y += 1
            grid[y][x] = '|'

        if y == max_y:
            continue

        x_left = x_right = x
        leak = False
        while x_left > 0 and grid[y][x_left - 1] not in blockers and grid[
                y + 1][x_left] in blockers:
            x_left -= 1
            grid[y][x_left] = '|'

        if grid[y + 1][x_left] not in blockers:
            points.append((x_left, y))
            leak = True

        while x_right < max_x and grid[y][
                x_right + 1] not in blockers and grid[y +
                                                      1][x_right] in blockers:
            x_right += 1
            grid[y][x_right] = '|'

        if grid[y + 1][x_right] not in blockers:
            points.append((x_right, y))
            leak = True

        if leak:
            continue
        else:
            grid[y][x_left:x_right + 1] = ['~'] * (x_right - x_left + 1)
            points.append((x, y - 1))
    return grid


def water_reached(grid):
    return sum(c in {'~', '|', '+'} for c in chain(*grid[1:len(grid) - 1]))


def water_left(grid):
    return sum(c in {'~'} for c in chain(*grid[1:len(grid) - 1]))


if __name__ == '__main__':
    grid, x_start = parse_input('./resources/day17.txt')
    result_grid = flow(grid, x_start)
    print('Part 1: {}'.format(water_reached(result_grid)))
    print('Part 2: {}'.format(water_left(result_grid)))
