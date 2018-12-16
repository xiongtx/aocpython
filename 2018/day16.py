import re
from collections import defaultdict, namedtuple

# Part 1

Case = namedtuple('Case', ['before', 'instruction', 'after'])


def parse_input(fname):
    cases = []
    with open(fname, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
        for i in range(0, len(lines), 4):
            before = map(int, re.findall(r'\d+', lines[i]))
            instruction = map(int, re.findall(r'\d+', lines[i + 1]))
            after = map(int, re.findall(r'\d+', lines[i + 2]))
            cases.append(Case(before, instruction, after))
    return cases


def execute(op, ios, registers):
    a, b, c = ios
    out = registers[:]

    if op == 'addr':
        out[c] = out[a] + out[b]
    elif op == 'addi':
        out[c] = out[a] + b
    elif op == 'mulr':
        out[c] = out[a] * out[b]
    elif op == 'muli':
        out[c] = out[a] * b
    elif op == 'banr':
        out[c] = out[a] & out[b]
    elif op == 'bani':
        out[c] = out[a] & b
    elif op == 'borr':
        out[c] = out[a] | out[b]
    elif op == 'bori':
        out[c] = out[a] | b
    elif op == 'setr':
        out[c] = out[a]
    elif op == 'seti':
        out[c] = a
    elif op == 'gtir':
        out[c] = 1 if a > out[b] else 0
    elif op == 'gtri':
        out[c] = 1 if out[a] > b else 0
    elif op == 'gtrr':
        out[c] = 1 if out[a] > out[b] else 0
    elif op == 'eqir':
        out[c] = 1 if a == out[b] else 0
    elif op == 'eqri':
        out[c] = 1 if out[a] == b else 0
    elif op == 'eqrr':
        out[c] = 1 if out[a] == out[b] else 0

    return out


ops = [
    'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr',
    'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
]


def three_or_more_ops(cases):
    return sum(
        sum([
            case.after == execute(op, case.instruction[1:], case.before)
            for op in ops
        ]) >= 3 for case in cases)


# Part 2


def parse_input_2(fname):
    with open(fname) as f:
        program = [map(int, re.findall(r'\d+', l)) for l in f.readlines()]
    return program


def valid_ops(case):
    return {
        op
        for op in ops
        if case.after == execute(op, case.instruction[1:], case.before)
    }


def opcode_numbers(cases):
    m = defaultdict(lambda: set(ops))
    for case in cases:
        i = case.instruction[0]
        m[i].intersection_update(valid_ops(case))
    op_m = {}
    while m:
        known = dict(filter(lambda (_, ops): len(ops) == 1, m.iteritems()))
        for k in known:
            op_m[k] = known[k].pop()
            del m[k]
            for i in m:
                m[i].discard(op_m[k])
    return op_m


def execute_program(cases, program):
    op_m = opcode_numbers(cases)
    registers = [0] * 4
    for l in program:
        op = op_m[l[0]]
        registers = execute(op, l[1:], registers)
    return registers[0]


if __name__ == '__main__':
    cases = parse_input('./resources/day16.txt')
    program = parse_input_2('./resources/day16_2.txt')
    print('Part 1: {}'.format(three_or_more_ops(cases)))
    print('Part 2: {}'.format(execute_program(cases, program)))
