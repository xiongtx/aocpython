import re


def parse_input(s):
    return re.match('(\w+) => (\w+)', s).groups()


def parse_inputs(ss):
    return [parse_input(s) for s in ss]


def num_transforms(rules, molecule):
    seen = set()
    for k, v in rules:
        indices = [m.start() for m in re.finditer('(?=' + k + ')', molecule)]
        for i in indices:
            seen.add(molecule[:i] + v + molecule[i + len(k):])
    return len(seen)


# See: https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4nsdd/
def num_steps(rules, molecule):
    """Note that this works b/c there's only a single way to generate the
    molecule from the rules.

    It doesn't necessarily work when there's more than one way to generate the
    output, e.g. for the HOHOHO example.

    """
    mol = molecule[::-1]
    reps = {v[::-1]: k[::-1] for k, v in rules}

    count = 0
    while mol != 'e':
        mol = re.sub('|'.join(reps.keys()), lambda m: reps[m.group()], mol, 1)
        count += 1

    return count


if __name__ == '__main__':
    with open('./resources/day19.txt', 'r') as f:
        ls = [l.rstrip() for l in f.readlines()]
        rules = parse_inputs(ls[:-2])
        molecule = ls[-1]
    print('Part 1: {}'.format(num_transforms(rules, molecule)))
    print('Part 2: {}'.format(num_steps(rules, molecule)))
