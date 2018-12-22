from collections import defaultdict
from functools import partial
import copy
import heapq
import sys


def split_group(s):
    idx = level = 0
    indices = [-1]
    while idx < len(s):
        if level == 0 and s[idx] == '|':
            indices.append(idx)
        if s[idx] == '(':
            level += 1
        elif s[idx] == ')':
            level -= 1
        idx += 1
    return [s[i + 1:j] for i, j in zip(indices, indices[1:] + [None])]


def matching_close(s):
    idx = level = 0
    while idx < len(s):
        if level == 0 and s[idx] == ')':
            return idx
        if s[idx] == '(':
            level += 1
        elif s[idx] == ')':
            level -= 1
        idx += 1


class Graph:
    def __init__(self):
        self.V = set()
        self.E = defaultdict(set)

    def add_edge(self, a, b):
        self.V.update([a, b])
        self.E[a].add(b)
        self.E[b].add(a)

    def shortest_paths(self):
        U = copy.copy(self.V)
        D = {v: sys.maxint for v in self.V}
        D[(0, 0)] = 0
        pq = [(0, (0, 0))]

        while pq:
            d, v = heapq.heappop(pq)
            U.discard(v)
            for u in filter(lambda n: n in U, self.E[v]):
                if D[u] > d + 1:
                    D[u] = d + 1
                heapq.heappush(pq, (D[u], u))
        return D

    def furthest_distance(self):
        return max(self.shortest_paths().values())

    def num_at_least_1000(self):
        return sum(d >= 1000 for d in self.shortest_paths().values())


def build_graph((x, y), regex):
    G = Graph()
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == '(':
            j = i + matching_close(regex[i + 1:]) + 1
            for g in map(
                    partial(build_graph, (x, y)), split_group(regex[i + 1:j])):
                G.V.update(g.V)
                for k, vs in g.E.iteritems():
                    G.E[k].update(vs)
            i = j + 1
        else:
            if c == 'N':
                G.add_edge((x, y), (x, y + 1))
                y = y + 1
            elif c == 'E':
                G.add_edge((x, y), (x + 1, y))
                x = x + 1
            elif c == 'S':
                G.add_edge((x, y), (x, y - 1))
                y = y - 1
            else:
                G.add_edge((x, y), (x - 1, y))
                x = x - 1
            i += 1
    return G


if __name__ == '__main__':
    with open('./resources/day20.txt') as f:
        regex = f.read().rstrip()[1:-1]
    G = build_graph((0, 0), regex)
    print('Part 1: {}'.format(G.furthest_distance()))
    print('Part 2: {}'.format(G.num_at_least_1000()))
