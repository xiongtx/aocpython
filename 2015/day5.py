import re

# Part 1

vowels = {'a', 'e', 'i', 'o', 'u'}
illegals = {'ab', 'cd', 'pq', 'xy'}


def is_nice(s):
    num_vowels = 0
    last_c = ''
    repeated_cs = False
    illegal = False
    for c in s:
        if c in vowels:
            num_vowels += 1
        if c == last_c:
            repeated_cs = True
        if last_c + c in illegals:
            illegal = True
        last_c = c
    return bool(num_vowels >= 3 and repeated_cs and not illegal)


def num_nice(nice_f, strs):
    n = 0
    for s in strs:
        if nice_f(s):
            n += 1
    return n


# Part 2


def is_nice_2(s):
    xyxy = re.search(r'(..).*\1', s)
    xyx = re.search(r'(.).\1', s)
    return bool(xyxy and xyx)


if __name__ == '__main__':
    with open('./resources/day5.txt', 'r') as f:
        strs = f.readlines()
    print('Part 1: {}'.format(num_nice(is_nice, strs)))
    print('Part 2: {}'.format(num_nice(is_nice_2, strs)))
