def increment_pw(s):
    if not s:
        return 'a'

    # Big skip if i, o, l
    confusing_idx = min(
        [s.index(c) if c in s else None for c in ['i', 'o', 'l']])
    if confusing_idx:
        return s[:confusing_idx] + chr(ord(s[confusing_idx]) +
                                       1) + 'a' * (len(s) - confusing_idx - 1)

    last = s[-1]
    if last == 'z':
        return increment_pw(s[:-1]) + 'a'
    else:
        return s[:-1] + chr(ord(last) + 1)


def contains_increasing_straight(s):
    for i in range(len(s) - 2):
        if ord(s[i]) + 2 == ord(s[i + 1]) + 1 == ord(s[i + 2]):
            return True
    return False


def excludes_confusing(s):
    return set('iol').isdisjoint(s)


def non_overlapping_pairs(s):
    return len({s[i:i + 2]
                for i in range(0,
                               len(s) - 1) if s[i] == s[i + 1]}) >= 2


def is_secure(s):
    return contains_increasing_straight(s) and excludes_confusing(
        s) and non_overlapping_pairs(s)


def next_secure_pw(s):
    while not is_secure(s):
        s = increment_pw(s)
    return s


if __name__ == '__main__':
    with open('./resources/day11.txt', 'r') as f:
        s = f.read().rstrip()
    pw1 = next_secure_pw(s)
    print('Part 1: {}'.format(pw1))
    print('Part 2: {}'.format(next_secure_pw(increment_pw(pw1))))

for f in os.listdir(os.curdir):
    match = re.match('day_(\d+)(.*)', f)
    if match:
        day, rest = match.groups()
        os.rename(f, 'day' + day + rest)
