import math
import re


def parse_instruction(s):
    op, a, b, c = re.match(r'([a-z]+) (\d+) (\d+) (\d+)', s).groups()
    return (op, int(a), int(b), int(c))


def parse_input(fname):
    with open(fname) as f:
        lines = [l.rstrip() for l in f.readlines()]
    ip_reg = int(re.findall(r'\d+', lines[0])[0])
    instructions = map(parse_instruction, lines[1:])
    return ip_reg, instructions


def execute(ip_reg, instructions, registers):
    out = registers[:]
    ip = registers[ip_reg]
    if not 0 <= ip < len(instructions):
        return 'DONE', out
    op, a, b, c = instructions[ip]

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

    out[ip_reg] += 1
    return 'CONTINUE', out


def execute_program(ip_reg, instructions, registers):
    state = 'START'
    while state != 'DONE':
        state, registers = execute(ip_reg, instructions, registers)
    return registers[0]


# Part 2

# The program calculates the sum of divisors of the value in the register
# above the IP register at the time of first register 0 change


def divisors(n):
    ds = []
    for i in range(1, int(math.ceil(math.sqrt(n)))):
        if n % i == 0:
            ds.extend([i, n / i])
    return ds


def start_val(ip_reg, instructions, registers):
    reg0 = registers[0]
    while reg0 == registers[0]:
        _, registers = execute(ip_reg, instructions, registers)
    return registers[ip_reg + 1]


def divisor_sum(n):
    return sum(divisors(n))


if __name__ == '__main__':
    ip_reg, instructions = parse_input('./resources/day19.txt')
    print('Part 1: {}'.format(execute_program(ip_reg, instructions, [0] * 6)))
    print('Part 2: {}'.format(
        divisor_sum(start_val(ip_reg, instructions, [1] + [0] * 5))))
