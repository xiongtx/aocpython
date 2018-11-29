# Part 1


def update_pos(x, y, ins):
    if ins == '^':
        y += 1
    elif ins == '>':
        x += 1
    elif ins == 'v':
        y -= 1
    else:
        x -= 1
    return (x, y)


def number_houses(instructions):
    x = y = 0
    visited = {(0, 0)}
    for ins in instructions:
        x, y = update_pos(x, y, ins)
        visited.add((x, y))
    return len(visited)


# Part 2


def number_houses_robo(instructions):
    x = y = x_robo = y_robo = 0
    visited = {(0, 0)}
    for i, ins in enumerate(instructions):
        if i % 2 == 0:
            x, y = update_pos(x, y, ins)
            visited.add((x, y))
        else:
            x_robo, y_robo = update_pos(x_robo, y_robo, ins)
            visited.add((x_robo, y_robo))
    return len(visited)


if __name__ == '__main__':
    with open('resources/day3.txt') as f:
        instructions = f.read()
    print('Part 1: {}'.format(number_houses(instructions)))
    print('Part 2: {}'.format(number_houses_robo(instructions)))
