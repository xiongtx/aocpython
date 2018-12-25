import re


def parse_line(s):
    return map(int, re.findall(r'-?\d+', s))


def parse_input(fname):
    with open(fname) as f:
        return [parse_line(l) for l in f.readlines()]


class UnionFind:
    """ Union-find data structure, taken from https://gist.github.com/SofiaGodovykh/18f60a3b9b3e6812c071456f61f9c5a6.
    """

    def __init__(self, n):
        self._id = list(range(n))
        self._sz = [1] * n

    def root(self, i):
        j = i
        while (j != self._id[j]):
            self._id[j] = self._id[self._id[j]]
            j = self._id[j]
        return j

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return
        if (self._sz[i] < self._sz[j]):
            self._id[i] = j
            self._sz[j] += self._sz[i]
        else:
            self._id[j] = i
            self._sz[i] += self._sz[j]


def manhattan_distance(c1, c2):
    return sum([abs(a - b) for a, b in zip(c1, c2)])


def num_constellations(coords):
    n = len(coords)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if manhattan_distance(coords[i], coords[j]) <= 3:
                uf.union(i, j)
    return len(set([uf.root(i) for i in range(n)]))


if __name__ == '__main__':
    coords = parse_input('./resources/day25.txt')
    print('Part 1: {}'.format(num_constellations(coords)))
