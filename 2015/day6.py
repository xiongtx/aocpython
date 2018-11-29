import re
import numpy as np

# Part 1


def parse_instruction(s):
    regexp = r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)'
    action, x1, y1, x2, y2 = re.search(regexp, s).groups()
    return (action, int(x1), int(y1), int(x2), int(y2))


def parse_instructions(ss):
    return [parse_instruction(s) for s in ss]


def num_lit(instructions):
    lights = np.zeros((1000, 1000))
    for action, x1, y1, x2, y2 in instructions:
        if action == 'turn on':
            lights[x1:x2 + 1, y1:y2 + 1] = 1
        elif action == 'turn off':
            lights[x1:x2 + 1, y1:y2 + 1] = 0
        else:
            lights[x1:x2 + 1, y1:y2 + 1] = 1 - lights[x1:x2 + 1, y1:y2 + 1]
    return np.count_nonzero(lights)


# Part 2


def turn_off(v):
    return v - 1 if v > 0 else 0


def total_brightness(instructions):
    lights = np.zeros((1000, 1000))
    turn_off_f = np.vectorize(turn_off)
    for action, x1, y1, x2, y2 in instructions:
        if action == 'turn on':
            lights[x1:x2 + 1, y1:y2 + 1] += 1
        elif action == 'turn off':
            lights[x1:x2 + 1, y1:y2 + 1] = turn_off_f(
                lights[x1:x2 + 1, y1:y2 + 1])
        else:
            lights[x1:x2 + 1, y1:y2 + 1] += 2
    return int(np.sum(lights))


if __name__ == '__main__':
    with open('./resources/day6.txt', 'r') as f:
        strs = [s.rstrip() for s in f.readlines()]
    instructions = parse_instructions(strs)
    print('Part 1: {}'.format(num_lit(instructions)))
    print('Part 2: {}'.format(total_brightness(instructions)))
