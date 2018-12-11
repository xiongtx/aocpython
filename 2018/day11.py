# Part 1


def power_level(x, y, n):
    rack_id = x + 10
    return (((rack_id * y + n) * rack_id) / 100) % 10 - 5


def largest_power_coord(n):
    grid = [[power_level(x, y, n) for y in range(1, 300 + 1)]
            for x in range(1, 300 + 1)]
    max_power = 0
    max_coords = None
    for x in range(300 - 3):
        for y in range(300 - 3):
            power = sum(
                grid[i][j] for i in range(x, x + 3) for j in range(y, y + 3))
            if power > max_power:
                max_power = power
                max_coords = (x + 1, y + 1)
    return max_coords


# Part 2


def power(x, y, w, power_m):
    if w == 1:
        return power_m[(x, y, 1)]
    else:
        return power_m[(x, y, 1)] + sum(
            power_m[(x, j, 1)] for j in range(y + 1, y + w)) + sum(
                power_m[(i, y, 1)]
                for i in range(x + 1, x + w)) + power_m[(x + 1, y + 1, w - 1)]


def largest_power_coord_any(n):
    power_m = {(x, y, 1): power_level(x + 1, y + 1, n)
               for x in range(300) for y in range(300)}
    max_power = 0
    max_coords = None
    for x in range(300)[::-1]:
        for y in range(300)[::-1]:
            for w in range(1, min(300 - x + 1, 300 - y + 1)):
                p = power(x, y, w, power_m)
                power_m[(x, y, w)] = p
                if p > max_power:
                    max_power = p
                    max_coords = (x + 1, y + 1, w)
    return max_coords


if __name__ == '__main__':
    with open('./resources/day11.txt', 'r') as f:
        n = int(f.read())
    print('Part 1: {}'.format(largest_power_coord(n)))
    print('Part 2: {}'.format(largest_power_coord_any(n)))
