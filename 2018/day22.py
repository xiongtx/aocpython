import re
import copy
from itertools import chain
import heapq
import sys

# Part 1


def parse_input(fname):
    with open(fname) as f:
        depth = map(int, re.findall(r'\d+', f.readline()))[0]
        target = map(int, re.findall(r'\d+', f.readline()))
    return depth, tuple(target)


def erosion_level((x, y), geology, depth):
    return (geology[y][x] + depth) % 20183


def geologic_index((x, y), erosion, target):
    if (x, y) == (0, 0):
        return 0
    elif (x, y) == target:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return erosion[y][x - 1] * erosion[y - 1][x]


def total_risk(depth, target):
    max_x = target[0] + 1
    max_y = target[1] + 1
    erosion = [[None] * max_x for _ in range(max_y)]
    geology = copy.deepcopy(erosion)
    for x in range(max_x):
        for y in range(max_y):
            geology[y][x] = geologic_index((x, y), erosion, target)
            erosion[y][x] = erosion_level((x, y), geology, depth)
    return sum(e % 3 for e in chain(*erosion))


# Part 2


def map_cave(depth, target):
    max_x = target[0] + 300
    max_y = target[1] + 300
    erosion = [[None] * max_x for _ in range(max_y)]
    geology = copy.deepcopy(erosion)
    cave = copy.deepcopy(erosion)
    for x in range(max_x):
        for y in range(max_y):
            geology[y][x] = geologic_index((x, y), erosion, target)
            erosion[y][x] = erosion_level((x, y), geology, depth)
            cave[y][x] = {
                0: 'rocky',
                1: 'wet',
                2: 'narrow'
            }.get(erosion[y][x] % 3)
    return cave


def adjacents((x, y), max_x, max_y):
    return filter(lambda (x, y): 0 <= x < max_x and 0 <= y < max_y,
                  [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)])


def manhattan_distance((x1, y1), (x2, y2)):
    return abs(x1 - x2) + abs(y1 - y2)


def min_time(depth, target):
    cave = map_cave(depth, target)
    max_y = len(cave)
    max_x = len(cave[0])
    all_equip = {'neither', 'torch', 'climbing gear'}
    unvisited = {(x, y, equip): True
                 for y in range(max_y) for x in range(max_x)
                 for equip in all_equip}
    distances = {k: sys.maxint for k in unvisited}
    distances[(0, 0, 'torch')] = 0
    pq = [(manhattan_distance((0, 0), target), 0, (0, 0), 'torch')]
    allowed_m = {
        'rocky': {'torch', 'climbing gear'},
        'wet': {'neither', 'climbing gear'},
        'narrow': {'neither', 'torch'}
    }
    while pq:
        _, d, (x, y), equip = heapq.heappop(pq)
        unvisited[(x, y, equip)] = False
        if (x, y) == target and equip == 'torch':
            return d
        for (i, j) in adjacents((x, y), max_x, max_y):
            estimate = manhattan_distance((i, j), target)
            for e in allowed_m[cave[y][x]].intersection(allowed_m[cave[j][i]]):
                if not unvisited[(i, j, e)]:
                    continue
                dist = d if e == equip else d + 7
                if distances[(i, j, e)] > dist + 1:
                    distances[(i, j, e)] = dist + 1
                    heapq.heappush(pq, (estimate + dist + 1, dist + 1,
                                        (i, j), e))


if __name__ == '__main__':
    depth, target = parse_input('./resources/day22.txt')
    print('Part 1: {}'.format(total_risk(depth, target)))
    print('Part 2: {}'.format(min_time(depth, target)))
