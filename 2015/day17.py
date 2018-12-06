# Part 1


def num_ways(containers, amount):
    if amount <= 0:
        return 0

    n = 0
    for i, x in enumerate(containers):
        a = amount - x
        if a == 0:
            n += 1
        else:
            n += num_ways(containers[i + 1:], a)
    return n


# Part 2


def container_combos(containers, amount):
    if amount <= 0:
        return []

    combos = []
    for i, x in enumerate(containers):
        a = amount - x
        if a == 0:
            combos.append([x])
        else:
            combos.extend(
                [[x] + l for l in container_combos(containers[i + 1:], a)])
    return combos


def num_min_combos(containers, amount):
    combos = container_combos(containers, amount)
    n = min(len(l) for l in combos)
    return sum(len(l) == n for l in combos)


if __name__ == '__main__':
    with open('./resources/day17.txt', 'r') as f:
        containers = [int(l) for l in f.readlines()]
    print('Part 1: {}'.format(num_ways(containers, 150)))
    print('Part 2: {}'.format(num_min_combos(containers, 150)))
