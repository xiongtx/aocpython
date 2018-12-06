from collections import Counter

# Part 1


def times(s, n):
    for _, v in Counter(s).iteritems():
        if v == n:
            return True
    return False


def checksum(boxes):
    num_twice = sum(times(x, 2) for x in boxes)
    num_thrice = sum(times(x, 3) for x in boxes)
    return num_twice * num_thrice


def differ_indices(b1, b2):
    return [i for i, (c1, c2) in enumerate(zip(b1, b2)) if c1 != c2]


def common_letters(boxes):
    for i, x in enumerate(boxes):
        for y in boxes[i + 1:]:
            indices = differ_indices(x, y)
            if len(indices) == 1:
                idx = indices[0]
                return x[:idx] + x[idx + 1:]


if __name__ == '__main__':
    with open('./resources/day2.txt', 'r') as f:
        boxes = [l.rstrip() for l in f.readlines()]
    print('Part 1: {}'.format(checksum(boxes)))
    print('Part 2: {}'.format(common_letters(boxes)))
