import copy
import re


def parse_input(s):
    cs = re.split(r',? ', s)
    if cs[0] in {'hlf', 'tpl', 'inc'}:
        return tuple(cs)
    elif cs[0] == 'jmp':
        return (cs[0], int(cs[1]))
    else:
        return (cs[0], cs[1], int(cs[2]))


def execute_ins(registers, pt, ins):
    registers = copy.copy(registers)
    if ins[0] == 'hlf':
        registers[ins[1]] /= 2
        pt += 1
    elif ins[0] == 'tpl':
        registers[ins[1]] *= 3
        pt += 1
    elif ins[0] == 'inc':
        registers[ins[1]] += 1
        pt += 1
    elif ins[0] == 'jmp':
        pt += ins[1]
    elif ins[0] == 'jie':
        if registers[ins[1]] % 2 == 0:
            pt += ins[2]
        else:
            pt += 1
    elif ins[0] == 'jio':
        if registers[ins[1]] == 1:
            pt += ins[2]
        else:
            pt += 1
    return registers, pt


def b_value(registers, instructions):
    pt = 0
    while 0 <= pt < len(instructions):
        registers, pt = execute_ins(registers, pt, instructions[pt])
    return registers['b']


if __name__ == '__main__':
    with open('./resources/day23.txt') as f:
        instructions = [parse_input(l.rstrip()) for l in f.readlines()]
    print('Part 1: {}'.format(b_value({'a': 0, 'b': 0}, instructions)))
    print('Part 2: {}'.format(b_value({'a': 1, 'b': 0}, instructions)))
