from collections import defaultdict
import re
import string

# Part 1


def parse_input(s):
    return re.findall(' ([A-Z]) ', s)


def graphs(edges):
    graph = defaultdict(list)
    rgraph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        rgraph[v].append(u)
    return (graph, rgraph)


def all_visited(u, rgraph, visited):
    for v in rgraph[u]:
        if not visited[v]:
            return False
    return True


def walk(v, (graph, rgraph), available, visited, L):
    if not visited[v]:
        L.append(v)
        visited[v] = True
        children = filter(lambda u: all_visited(u, rgraph, visited), graph[v])
        nexts = sorted(set(children) | set(available))
        for u in nexts:
            if not visited[u]:
                walk(u, (graph, rgraph), nexts[1:], visited, L)


def order(edges):
    us = map(lambda t: t[0], edges)
    vs = map(lambda t: t[1], edges)
    inits = sorted(set(us) - set(vs))
    graph, rgraph = graphs(edges)
    L = []
    visited = defaultdict(lambda: False)
    for v in inits:
        walk(v, (graph, rgraph), inits[1:], visited, L)
    return string.join(L, '')


# Part 2


def prereqs_done(u, rgraph, times):
    for v in rgraph[u]:
        if times[v] > 0:
            return False
    return True


def time_step(available, worker_map, (graph, rgraph), times):
    workers_free = [k for k, v in worker_map.iteritems() if not v]
    work_free = sorted(set(available) - set(worker_map.values()))

    for i, v in zip(workers_free, work_free[:len(workers_free)]):
        worker_map[i] = v

    for v in (x for x in worker_map.itervalues() if x):
        times[v] -= 1
        if times[v] == 0:
            for i, u in worker_map.iteritems():
                if u == v:
                    worker_map[i] = None
            available = filter(lambda x: x != v, available)
            available.extend(
                filter(
                    lambda u: times[u] > 0 and prereqs_done(u, rgraph, times),
                    graph[v]))
    return sorted(set(available))


def time(edges, n, base_time):
    us = set(map(lambda t: t[0], edges))
    vs = set(map(lambda t: t[1], edges))
    available = sorted(us - vs)
    graph, rgraph = graphs(edges)
    times = {v: base_time + ord(v) - ord('A') + 1 for v in us | vs}
    worker_map = {i: None for i in range(n)}
    t = 0
    while available:
        available = time_step(available, worker_map, (graph, rgraph), times)
        t += 1
    return t


if __name__ == '__main__':
    with open('./resources/day7.txt', 'r') as f:
        edges = [parse_input(l) for l in f.readlines()]
    print('Part 1: {}'.format(order(edges)))
    print('Part 2: {}'.format(time(edges, 5, 60)))
