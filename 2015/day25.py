def row_col_num(row, col):
    n = row + col - 1
    return (1 + (n - 1)) * (n - 1) / 2 + col


def code_at(row, col):
    code = 20151125
    for i in range(1, row_col_num(row, col)):
        code = (code * 252533) % 33554393
    return code


if __name__ == '__main__':
    print('Part 1: {}'.format(code_at(2947, 3029)))
