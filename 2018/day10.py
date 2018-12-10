import re
import matplotlib.pyplot as plt

def parse_input(s):
    return map(int, re.findall('-?\d+', s))


def update_inputs(inputs, n):
    return [(x + n * dx, y + n * dy, dx, dy) for x, y, dx, dy in inputs]


def message_animate(inputs, start, stop, step):
    inputs = update_inputs(inputs, start)
    for i in range(0, stop - start, step):
        xs = map(lambda t: t[0], inputs)
        ys = map(lambda t: -t[1], inputs)
        plt.plot(xs, ys, 'bo')
        plt.draw()
        plt.pause(0.0001)
        plt.clf()
        inputs = update_inputs(inputs, step)

def message(inputs, n):
    inputs = update_inputs(inputs, n)
    xs = map(lambda t: t[0], inputs)
    ys = map(lambda t: -t[1], inputs)
    plt.plot(xs, ys, 'bo')
    plt.show()


if __name__ == '__main__':
    with open('./resources/day10.txt', 'r') as f:
        inputs = [parse_input(s) for s in f.readlines()]
    print('Part 1: {}'.format('LKPHZHHJ'))
    print('Part 2: {}'.format(10159))
