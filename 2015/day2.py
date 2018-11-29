import re

# Part 1


def parse_dims(s):
    return [int(n) for n in re.findall(r'[0-9]+', s)]


def box_area(l, w, h):
    return 2 * l * w + 2 * w * h + 2 * l * h + min(l * w, w * h, h * l)


def total_area(all_dims):
    return sum([box_area(l, w, h) for l, w, h in all_dims])


# Part 2


def ribbon_length(l, w, h):
    wrap_length = min(2 * (l + w), 2 * (w + h), 2 * (h + l))
    bow_length = l * w * h
    return wrap_length + bow_length


def total_length(all_dims):
    return sum([ribbon_length(l, w, h) for l, w, h in all_dims])


if __name__ == '__main__':
    with open('resources/day2.txt') as f:
        all_dims = [parse_dims(s) for s in f.readlines()]
    print('Part 1: {}'.format(total_area(all_dims)))
    print('Part 2: {}'.format(total_length(all_dims)))
