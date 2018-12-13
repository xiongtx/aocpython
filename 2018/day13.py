import copy


def carts_map(tracks):
    carts = {'<', '>', '^', 'v'}
    positions = [(y, x) for y in range(len(tracks))
                 for x in range(len(tracks[0])) if tracks[y][x] in carts]
    return {(y, x): (tracks[y][x], 'left') for y, x in positions}


def parse_input(fname):
    with open(fname, 'r') as f:
        tracks = [list(l[:-1]) for l in f.readlines()]
    carts_m = carts_map(tracks)
    for y in range(len(tracks)):
        for x in range(len(tracks[0])):
            c = tracks[y][x]
            if c in {'<', '>'}:
                tracks[y][x] = '-'
            elif c in {'^', 'v'}:
                tracks[y][x] = '|'
    return tracks, carts_m


def move(tracks, carts_m, (y, x)):
    cart, direction = carts_m[(y, x)]
    pos_m = {
        '^': (y - 1, x),
        'v': (y + 1, x),
        '<': (y, x - 1),
        '>': (y, x + 1)
    }
    i, j = pos_m[cart]
    c = tracks[i][j]
    if (i, j) in carts_m.keys():
        cart = 'X'
        direction = None
    elif c == '/':
        cart = {'^': '>', '>': '^', 'v': '<', '<': 'v'}.get(cart)
    elif c == '\\':
        cart = {'^': '<', '>': 'v', 'v': '>', '<': '^'}.get(cart)
    elif c == '+':
        if direction == 'left':
            cart = {'^': '<', '>': '^', 'v': '>', '<': 'v'}.get(cart)
        elif direction == 'right':
            cart = {'^': '>', '>': 'v', 'v': '<', '<': '^'}.get(cart)
        direction = {
            'left': 'straight',
            'straight': 'right',
            'right': 'left'
        }.get(direction)

    new_carts_m = copy.copy(carts_m)
    del new_carts_m[(y, x)]
    new_carts_m[(i, j)] = (cart, direction)

    return new_carts_m, (i, j)


def first_crash_coords(tracks, carts_m):
    while True:
        for pos in sorted(carts_m.keys()):
            new_carts_m, new_pos = move(tracks, carts_m, pos)
            new_cart, _ = new_carts_m[new_pos]
            if new_cart == 'X':
                y, x = new_pos
                return (x, y)
            else:
                carts_m = new_carts_m


def last_cart_coords(tracks, carts_m):
    while len(carts_m.keys()) >= 2:
        for pos in sorted(carts_m.keys()):
            if pos in carts_m.keys():
                new_carts_m, _ = move(tracks, carts_m, pos)
                carts_m = {
                    pos: (cart, direction)
                    for pos, (cart, direction) in new_carts_m.iteritems()
                    if cart != 'X'
                }

    if not carts_m:
        raise Exception('No remaining cart')

    (y, x) = carts_m.keys()[0]
    return (x, y)


if __name__ == '__main__':
    tracks, carts_m = parse_input('./resources/day13.txt')
    print('Part 1: {}'.format(first_crash_coords(tracks, carts_m)))
    print('Part 2: {}'.format(last_cart_coords(tracks, carts_m)))
