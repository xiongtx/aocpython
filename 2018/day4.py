from collections import defaultdict
from dateutil.parser import parse
import datetime
import re

# Part 1


def parse_input(s):
    s1, s2 = s.split('] ')
    time = parse(s1[1:])
    ids = re.findall('(\d+)', s2)
    return (time, ids[0] if ids else s2)


def parse_events(events):
    guard = None
    sleep_start = None
    guards_m = defaultdict(list)

    for time, data in events:
        if data == 'falls asleep':
            sleep_start = time
        elif data == 'wakes up':
            guards_m[guard].append((sleep_start, time))
        else:
            guard = data

    return guards_m


def compare_events((t1, d1), (t2, d2)):
    states = ['wakes up', 'falls asleep']
    d1_idx = states.index(d1) if d1 in states else -1
    d2_idx = states.index(d2) if d2 in states else -1
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        if d1_idx < d2_idx:
            return -1
        elif d1_idx > d2_idx:
            return 1
        else:
            return 0


def total_sleep(times):
    return sum([end - start for start, end in times], datetime.timedelta())


def most_frequent_minute(times):
    minutes = [0] * 60
    for start, end in times:
        for i in range(start.minute, end.minute):
            minutes[i] += 1
    return sorted(enumerate(minutes), key=lambda t: t[1], reverse=True)[0]


def strategy_1(events):
    guard_m = parse_events(events)
    _, guard = sorted(
        ((total_sleep(times), guard) for guard, times in guard_m.iteritems()),
        reverse=True)[0]
    minute, _ = most_frequent_minute(guard_m[guard])

    return int(guard) * minute


# Part 2


def strategy_2(events):
    guard_m = parse_events(events)
    guard_minutes = []

    for guard, times in guard_m.iteritems():
        minute, n = most_frequent_minute(times)
        guard_minutes.append((n, minute, guard))

    _, minute, guard = sorted(guard_minutes, reverse=True)[0]
    return int(guard) * minute


if __name__ == '__main__':
    with open('./resources/day4.txt', 'r') as f:
        events = sorted([parse_input(l.rstrip()) for l in f.readlines()],
                        cmp=compare_events)
    print('Part 1: {}'.format(strategy_1(events)))
    print('Part 2: {}'.format(strategy_2(events)))
