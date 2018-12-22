# Shamelessly taken from
# https://www.reddit.com/r/adventofcode/comments/a86jgt/2018_day_21_solutions/ec8fzvh/,
# since I'm 💩 at translating assembly.

d = 0
s = set()
part1 = False
while True:
    e = d | 0x10000
    d = 1107552
    while True:
        f = e & 0xFF
        d += f
        d &= 0xFFFFFF
        d *= 65899
        d &= 0xFFFFFF
        if (256 > e):
            if part1:
                print(d)
                exit(0)
            else:
                if d not in s:
                    print(d)
                s.add(d)
                break
        # the following code was the optimised part
        e = e // 256
