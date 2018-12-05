import operator


def qe(weights):
    return reduce(operator.mul, weights)


def combos_recurse(weights, W, n, L_m):
    if W == 0:
        L_m['max'] = min(L_m['max'], n)
        return [[]]

    if not weights or n > L_m['max']:
        return []

    return [
        l + [w] for i, w in enumerate(weights)
        for l in combos_recurse(weights[i + 1:], W - w, n + 1, L_m)
    ]


def combos(weights, W, num_pkgs):
    cs = combos_recurse(
        sorted(weights, reverse=True), W, 0, {'max': len(weights) / num_pkgs})
    cs_sorted = sorted(cs, key=len)
    return [l for l in cs_sorted if len(l) == len(cs_sorted[0])]


def min_combo_qe(weights, num_pkgs):
    W = sum(weights) / num_pkgs
    return qe(sorted(combos(weights, W, num_pkgs), key=qe)[0])


if __name__ == '__main__':
    with open('./resources/day24.txt') as f:
        weights = [int(l) for l in f.readlines()]
    print('Part 1: {}'.format(min_combo_qe(weights, 3)))
    print('Part 2: {}'.format(min_combo_qe(weights, 4)))
