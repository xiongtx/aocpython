import heapq
import re

# Part 1


def parse_input(s):
    x, c, d, f, t, cal = re.match(
        '(\w+): capacity (-?\d), durability (-?\d), flavor (-?\d), texture (-?\d), calories (-?\d)',
        s).groups()
    return (x, int(c), int(d), int(f), int(t), int(cal))


def parse_inputs(ss):
    return [parse_input(s) for s in ss]


def score(cookies, amounts):
    capacity = durability = flavor = texture = 0
    for (_, c, d, f, t, _), n in zip(cookies, amounts):
        capacity += c * n
        durability += d * n
        flavor += f * n
        texture += t * n
    return max(capacity, 0) * max(durability, 0) * max(flavor, 0) * max(
        texture, 0)


def adj_amounts(amounts):
    mvs = []
    indices = range(len(amounts))
    k_m = {100: [-1], 0: [1]}
    for i in indices:
        for k in k_m.get(amounts[i], [-1, 1]):
            for j in indices[i + 1:]:
                if 0 <= amounts[j] - k <= 100:
                    mvs.append(amounts[:i] + (amounts[i] + k, ) +
                               amounts[i + 1:j] + (amounts[j] - k, ) +
                               amounts[j + 1:])
    return mvs


def max_score(cookies):
    n = len(cookies)
    init_amount = (100 / n, ) * (n - 1) + (100 - 100 / n * (n - 1), )
    max_s = init_s = score(cookies, init_amount)
    pq = [(init_s, init_amount)]
    seen = set(init_amount)
    while pq:
        _, current_a = heapq.heappop(pq)
        for amount in adj_amounts(current_a):
            s = score(cookies, amount)
            if s >= max_s and amount not in seen:
                heapq.heappush(pq, (s, amount))
                seen.add(amount)
                max_s = s
    return max_s


# Part 2


def calories(cookies, amount):
    return sum(cookie[-1] * n for cookie, n in zip(cookies, amount))


def max_score_calories(cookies):
    n = len(cookies)
    init_amount = (100 / n, ) * (n - 1) + (100 - 100 / n * (n - 1), )
    init_s = score(cookies, init_amount)
    max_s = -1
    pq = [(init_s, init_amount)]
    seen = set(init_amount)
    while pq:
        _, current_a = heapq.heappop(pq)
        for amount in adj_amounts(current_a):
            s = score(cookies, amount)
            if s >= max_s and amount not in seen:
                heapq.heappush(pq, (s, amount))
                seen.add(amount)
                if calories(cookies, amount) == 500:
                    max_s = s
    return max_s


if __name__ == '__main__':
    with open('./resources/day15.txt', 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    cookies = parse_inputs(lines)
    print('Part 1: {}'.format(max_score(cookies)))
    print('Part 2: {}'.format(max_score_calories(cookies)))
