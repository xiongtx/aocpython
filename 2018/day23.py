import re
from z3 import If, Int, Optimize


def parse_line(s):
    return tuple(map(int, re.findall(r'-?\d+', s)))


def parse_input(fname):
    with open(fname) as f:
        return [parse_line(l) for l in f.readlines()]


def dist((x1, y1, z1), (x2, y2, z2)):
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def max_in_range(bots):
    x_max, y_max, z_max, r_max = sorted(
        bots, key=lambda t: t[3], reverse=True)[0]
    return sum(
        dist((x, y, z), (x_max, y_max, z_max)) <= r_max for x, y, z, r in bots)


# Part 2
# Shamelessly stolen from https://github.com/msullivan/advent-of-code/blob/master/2018/23b.py
# Note to self: learn something about SAT solvers / theorem provers


def z3_abs(x):
    return If(x >= 0, x, -x)


def z3_dist(x, y):
    return z3_abs(x[0] - y[0]) + z3_abs(x[1] - y[1]) + z3_abs(x[2] - y[2])


def optimum_dist(bots):
    x = Int('x')
    y = Int('y')
    z = Int('z')
    cost_expr = x * 0
    for i, j, k, r in bots:
        cost_expr += If(z3_dist((x, y, z), (i, j, k)) <= r, 1, 0)
    opt = Optimize()
    opt.maximize(cost_expr)
    opt.minimize(z3_dist((0, 0, 0), (x, y, z)))
    opt.check()
    model = opt.model()
    coords = (model[x].as_long(), model[y].as_long(), model[z].as_long())
    return dist((0, 0, 0), coords)


if __name__ == '__main__':
    bots = parse_input('./resources/day23.txt')
    print('Part 1: {}'.format(max_in_range(bots)))
    print('Part 2: {}'.format(optimum_dist(bots)))
