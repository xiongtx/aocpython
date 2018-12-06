import itertools

# Part 1


def neighbors((x, y), n):
    xys = []
    for a in [x - 1, x, x + 1]:
        for b in [y - 1, y, y + 1]:
            if 0 <= a < n and 0 <= b < n and (a, b) != (x, y):
                xys.append((a, b))
    return xys


def lights_on(grid, steps):
    n = len(grid)
    for _ in range(steps):
        new_grid = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                num_on = sum(
                    grid[x][y] == '#' for x, y in neighbors((i, j), n))
                if grid[i][j] == '#':
                    new_grid[i][j] = '#' if num_on in {2, 3} else '.'
                else:
                    new_grid[i][j] = '#' if num_on == 3 else '.'
        grid = new_grid
    return sum(light == '#' for light in itertools.chain(*new_grid))


# Part 2


def lights_on_corners(grid, steps):
    n = len(grid)
    corners = {(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)}
    for i, j in corners:
        grid[i][j] = '#'
    for _ in range(steps):
        new_grid = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i, j) in corners:
                    new_grid[i][j] = '#'
                else:
                    num_on = sum(
                        grid[x][y] == '#' for x, y in neighbors((i, j), n))
                    if grid[i][j] == '#':
                        new_grid[i][j] = '#' if num_on in {2, 3} else '.'
                    else:
                        new_grid[i][j] = '#' if num_on == 3 else '.'
        grid = new_grid
    return sum(light == '#' for light in itertools.chain(*new_grid))


if __name__ == '__main__':
    with open('./resources/day18.txt', 'r') as f:
        grid = [list(l.rstrip()) for l in f.readlines()]
    print('Part 1: {}'.format(lights_on(grid, 100)))
    print('Part 2: {}'.format(lights_on_corners(grid, 100)))
