import re

# Part 2

gift_giver = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}


def parse_input(s):
    return {
        category: int(n)
        for _, category, n in re.findall('((\w+): (\d+),? ?)', s)
    }


def parse_inputs(ss):
    return [parse_input(s) for s in ss]


def right_sue(sue, giver):
    for k, v in sue.iteritems():
        if v != giver[k]:
            return False
    return True


def gift_giver_num(sues, giver, right_f):
    for i, sue in enumerate(sues):
        if right_f(sue, giver):
            return i + 1

# Part 2

def real_right_sue(sues, giver):
    for k, v in sues.iteritems():
        if k in {'cats', 'trees'}:
            if not v > giver[k]:
                return False
        elif k in {'pomeranians', 'goldfish'}:
            if not v < giver[k]:
                return False
        else:
            if v != giver[k]:
                return False
    return True


if __name__ == '__main__':
    with open('./resources/day16.txt', 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    sues = parse_inputs(lines)
    print('Part 1: {}'.format(gift_giver_num(sues, gift_giver, right_sue)))
    print('Part 2: {}'.format(gift_giver_num(sues, gift_giver, real_right_sue)))
