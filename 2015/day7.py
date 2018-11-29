from collections import defaultdict
import operator
import re

# Part 1


def parse_instruction(s):
    assign_match = re.match(r'(\d+|\w+) -> (\w+)', s)
    if assign_match:
        x1, x2 = assign_match.groups()
        x1 = int(x1) if unicode(x1).isnumeric() else x1
        return ('ASSIGN', x1, x2)
    infix_match = re.match(
        r'(\d+|\w+) (AND|OR|LSHIFT|RSHIFT) (\d+|\w+) -> (\w+)', s)
    if infix_match:
        x1, op, x2, x3 = infix_match.groups()
        x1 = int(x1) if unicode(x1).isnumeric() else x1
        x2 = int(x2) if unicode(x2).isnumeric() else x2
        return (op, x1, x2, x3)
    not_match = re.match(r'NOT (\w+) -> (\w+)', s)
    if not_match:
        x1, x2 = not_match.groups()
        return ('NOT', x1, x2)


def parse_instructions(ss):
    return [parse_instruction(s) for s in ss]


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.V = set()

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.V.update([u, v])

    def sort_util(self, v, visited, stack):
        visited[v] = True
        for w in self.graph[v]:
            if not visited[w]:
                self.sort_util(w, visited, stack)
        stack.append(v)

    def tsort(self):
        visited = defaultdict(lambda: False)
        stack = []
        for v in self.V:
            if not visited[v]:
                self.sort_util(v, visited, stack)
        stack.reverse()
        return stack


op_map = {
    'AND': operator.and_,
    'OR': operator.or_,
    'LSHIFT': operator.lshift,
    'RSHIFT': operator.rshift
}


def execute_instruction(state, ins):
    op = ins[0]
    if op is 'ASSIGN':
        _, x1, target = ins
        state[target] = state[x1] if isinstance(x1, str) else x1
    elif op in {'AND', 'OR', 'LSHIFT', 'RSHIFT'}:
        _, x1, x2, target = ins
        x1 = state[x1] if isinstance(x1, str) else x1
        x2 = state[x2] if isinstance(x2, str) else x2
        state[target] = op_map[op](x1, x2)
    elif op is 'NOT':
        _, x1, target = ins
        x1 = state[x1] if isinstance(x1, str) else x1
        state[target] = ~x1


def sort_vs(instructions):
    g = Graph()
    for ins in instructions:
        op = ins[0]
        if op is 'ASSIGN':
            _, x1, target = ins
            if isinstance(x1, str):
                g.addEdge(x1, target)
        if op in {'AND', 'OR', 'LSHIFT', 'RSHIFT'}:
            _, x1, x2, target = ins
            if isinstance(x1, str):
                g.addEdge(x1, target)
            if isinstance(x2, str):
                g.addEdge(x2, target)
        elif op is 'NOT':
            _, x1, target = ins
            if isinstance(x1, str):
                g.addEdge(x1, target)
    return g.tsort()


def a_out(instructions):
    ins_map = {}
    for ins in instructions:
        ins_map[ins[-1]] = ins

    state = {}
    for v in sort_vs(instructions):
        execute_instruction(state, ins_map[v])
    return state['a']


# Part 2


def a_out_overriding_b(instructions, bval):
    ins_map = {}
    for ins in instructions:
        ins_map[ins[-1]] = ins
    ins_map['b'] = ('ASSIGN', bval, 'b')

    state = {}
    for v in sort_vs(instructions):
        execute_instruction(state, ins_map[v])
    return state['a']


if __name__ == '__main__':
    with open('./resources/day7.txt', 'r') as f:
        strs = [s.rstrip() for s in f.readlines()]
    instructions = parse_instructions(strs)
    print('Part 1: {}'.format(a_out(instructions)))
    print('Part 2: {}'.format(a_out_overriding_b(instructions, 3176)))
