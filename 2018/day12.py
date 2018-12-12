import re
import string

# Part 2


def parse_input(s):
    return re.match(r'(.+) => (.+)', s).groups()


def parse_file(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
        state = list(lines[0][15:].rstrip())
        rules = {}
        for l in lines[2:]:
            left, right = parse_input(l)
            rules[left] = right
        return state, rules


def apply_rules(state, zero_idx, rules):
    extended_state = ['.'] * 4 + state + ['.'] * 4
    new_state = ['.'] * len(extended_state)
    for i in range(2, len(extended_state) - 2):
        segment = string.join(extended_state[i - 2:i + 3], '')
        new_state[i] = rules.get(segment, '.')
    first_idx = new_state.index('#')
    last_idx = new_state[::-1].index('#')
    return new_state[first_idx:len(new_state) -
                     last_idx], zero_idx + 4 - first_idx


def sum_pot_nums(state, rules, n):
    zero_idx = 0
    for _ in range(n):
        state, zero_idx = apply_rules(state, zero_idx, rules)
    return sum(i - zero_idx for i, c in enumerate(state) if c == '#')


# Part 2


def sum_pot_nums_large(state, rules, n):
    str_n = str(n)
    base = str(sum_pot_nums(state, rules, int(str_n[0] + '000')))
    return int(base[0] + '0' * (str_n.count('0') - 3) + base[1:])


if __name__ == '__main__':
    state, rules = parse_file('./resources/day12.txt')
    print('Part 1: {}'.format(sum_pot_nums(state, rules, 20)))
    print('Part 2: {}'.format(sum_pot_nums_large(state, rules, int(5E10))))
