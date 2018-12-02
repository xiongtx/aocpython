# Part 1


def min_house(n):
    N = n / 10 + 1
    houses = [0] * N
    for i in range(1, N):
        for j in range(i, N, i):
            houses[j] += i * 10
    for i, v in enumerate(houses):
        if v >= n:
            return i


# Part 2


def min_house_50(n):
    N = n / 11 + 1
    houses = [0] * N
    for i in range(1, N):
        for j in range(i, min(N, 50 * i + 1), i):
            houses[j] += i * 11
    for i, v in enumerate(houses):
        if v >= n:
            return i


if __name__ == '__main__':
    with open('./resources/day20.txt', 'r') as f:
        n = int(f.read())
    print('Part 1: {}'.format(min_house(n)))
    print('Part 2: {}'.format(min_house_50(n)))
