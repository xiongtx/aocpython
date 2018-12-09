from collections import defaultdict, deque

# Part 1


def high_score(n_p, n_m):
    marbles = [0]
    player = current = 0
    scores = defaultdict(int)
    for i in range(1, n_m + 1):
        player = (player + 1) % n_p
        if i % 23 == 0:
            idx = (current - 7) % len(marbles)
            scores[player] += i + marbles.pop(idx)
            current = idx % len(marbles)
        else:
            idx = 1 if current == len(marbles) - 1 else current + 2
            marbles.insert(idx, i)
            current = idx
    return max(scores.values())


# Part 2


def high_score_large(n_p, n_m):
    marbles = deque([0])
    player = 0
    scores = defaultdict(int)
    for i in range(1, n_m + 1):
        player = (player + 1) % n_p
        if i % 23 == 0:
            marbles.rotate(7)
            scores[player] += i + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(i)
    return max(scores.values()) if scores else 0


if __name__ == '__main__':
    print('Part 1: {}'.format(high_score(419, 72164)))
    print('Part 2: {}'.format(high_score_large(419, 7216400)))
