from hashlib import md5

# Part 1


def min_5_zeros(secret):
    i = 1
    while not md5(secret + str(i)).hexdigest().startswith('00000'):
        i += 1
    return i


# Part 2


def min_6_zeros(secret):
    i = 1
    while not md5(secret + str(i)).hexdigest().startswith('000000'):
        i += 1
    return i


if __name__ == '__main__':
    with open('./resources/day4.txt', 'r') as f:
        secret = f.read().rstrip()
    print('Part 1: {}'.format(min_5_zeros(secret)))
    print('Part 2: {}'.format(min_6_zeros(secret)))
