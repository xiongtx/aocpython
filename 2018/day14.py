def ten_recipes_after(str_n):
    n = int(str_n)
    recipes = '37'
    i = 0
    j = 1
    while len(recipes) < n + 10:
        r1 = recipes[i]
        r2 = recipes[j]
        recipes = recipes + str(int(r1) + int(r2))
        i = (i + 1 + int(r1)) % len(recipes)
        j = (j + 1 + int(r2)) % len(recipes)
    return recipes[n:n + 10]


def num_recipes_before(str_n):
    recipes = '37'
    i = 0
    j = 1
    idx = None
    while not idx:
        r1 = recipes[i]
        r2 = recipes[j]
        new_recipes = str(int(r1) + int(r2))
        old_len = len(recipes)
        recipes = recipes + new_recipes
        i = (i + 1 + int(r1)) % len(recipes)
        j = (j + 1 + int(r2)) % len(recipes)
        try:
            idx = recipes.index(str_n, old_len - len(str_n) + 1)
        except ValueError:
            pass
    return idx


if __name__ == '__main__':
    with open('./resources/day14.txt', 'r') as f:
        str_n = f.read()
    print('Part 1: {}'.format(ten_recipes_after(str_n)))
    print('Part 2: {}'.format(num_recipes_before(str_n)))
