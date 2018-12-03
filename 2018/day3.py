import re

# Part 1


def parse_input(s):
    ID, left, top, width, height = re.match(
        r'#(\S+) @ (\d+),(\d+): (\d+)x(\d+)', s).groups()
    return (ID, int(left), int(top), int(width), int(height))


def overlapped_area(claims):
    grid = [[0] * 1000 for _ in range(1000)]
    for _, l, t, w, h in claims:
        for i in range(t, t + h):
            for j in range(l, l + w):
                grid[i][j] += 1
    return sum(1 for l in grid for x in l if x > 1)


# Part 2


def overlaps(c1, c2):
    _, l1, t1, w1, h1 = c1
    _, l2, t2, w2, h2 = c2
    (x1, y1), (x2, y2) = (t1, l1), (t1 + h1, l1 + w1)
    (x3, y3), (x4, y4) = (t2, l2), (t2 + h2, l2 + w2)

    if x2 <= x3 or x4 <= x1:
        return False
    elif y2 <= y3 or y4 <= y1:
        return False
    return True


def non_overlapping_claim(claims):
    ids = {c[0] for c in claims}
    for c1 in claims:
        for c2 in claims:
            if c1 != c2 and overlaps(c1, c2):
                ids.difference_update([c1[0], c2[0]])
            if len(ids) == 1:
                return ids.pop()


if __name__ == '__main__':
    with open('./resources/day3.txt', 'r') as f:
        claims = [parse_input(l.rstrip()) for l in f.readlines()]
    print('Part 1: {}'.format(overlapped_area(claims)))
    print('Part 2: {}'.format(non_overlapping_claim(claims)))
