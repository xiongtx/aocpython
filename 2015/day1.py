# Part 1
def floors(instructions):
    return instructions.count('(') - instructions.count(')')


# Part 2
def basement_position(instructions):
    floor = 0
    for i, c in enumerate(instructions):
        if c == '(':
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            return i + 1


if __name__ == '__main__':
    with open('./resources/day1.txt', 'r') as f:
        instructions = f.read()
    print('Part 1: {}'.format(floors(instructions)))
    print('Part 2: {}'.format(basement_position(instructions)))
