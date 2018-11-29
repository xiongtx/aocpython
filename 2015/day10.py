# Part 1


def look_and_say(s, n):
    if n == 0:
        return s

    k = 0
    prev_c = s[0]
    new_s = ''
    for c in s:
        if c != prev_c:
            new_s += str(k) + prev_c
            prev_c = c
            k = 1
        else:
            k += 1
    if k > 0:
        new_s += str(k) + prev_c
    return look_and_say(new_s, n - 1)


if __name__ == '__main__':
    with open('./resources/day10.txt', 'r') as f:
        s = f.read().rstrip()
    print('Part 1: {}'.format(len(look_and_say(s, 40))))
    print('Part 2: {}'.format(len(look_and_say(s, 50))))
