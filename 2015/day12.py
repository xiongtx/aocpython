import json

# Part 1


def sum_obj(obj):
    total = 0
    if isinstance(obj, dict):
        for k, v in obj.iteritems():
            total += sum_obj(k) + sum_obj(v)
    elif isinstance(obj, list):
        for e in obj:
            total += sum_obj(e)
    elif isinstance(obj, (int, float)):
        total += obj
    return total


def sum_objs(objs, sum_f):
    return sum([sum_f(obj) for obj in objs])


# Part 2


def sum_excluding_red(obj):
    total = 0
    if isinstance(obj, dict):
        for k, v in obj.iteritems():
            if v == 'red':
                return 0
            else:
                total += sum_excluding_red(k) + sum_excluding_red(v)
    elif isinstance(obj, list):
        for e in obj:
            total += sum_excluding_red(e)
    elif isinstance(obj, (int, float)):
        total += obj
    return total


if __name__ == '__main__':
    with open('./resources/day12.txt', 'r') as f:
        lines = f.readlines()
    data = [json.loads(l) for l in lines]
    print('Part 1: {}'.format(sum_objs(data, sum_obj)))
    print('Part 2: {}'.format(sum_objs(data, sum_excluding_red)))
