import re
import string


def react(s):
    regex = string.join([
        c1 + c2 for c1 in string.ascii_letters
        for c2 in string.ascii_letters if abs(ord(c1) - ord(c2)) == 32
    ], '|')
    prev_s = None
    while s != prev_s:
        prev_s = s
        s = re.sub(regex, '', s)
    return s


def min_remove_react_length(s):
    min_l = len(s)
    for pair in [c + '|' + c.upper() for c in string.ascii_lowercase]:
        l = len(react(re.sub(pair, '', s)))
        if l < min_l:
            min_l = l
    return min_l


if __name__ == '__main__':
    with open('./resources/day5.txt', 'r') as f:
        s = f.read().rstrip()
    print('Part 1: {}'.format(len(react(s))))
    print('Part 2: {}'.format(min_remove_react_length(s)))
