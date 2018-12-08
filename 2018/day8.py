# Part 1


def metadata_sum_at(i, nums):
    n_c = nums[i]
    n_m = nums[i + 1]
    if n_c == 0:
        m_start = i + 2
        m_end = m_start + n_m
        return (sum(nums[m_start:m_end]), m_end)
    else:
        total = 0
        c_start = i + 2
        for _ in range(n_c):
            c_total, c_start = metadata_sum_at(c_start, nums)
            total += c_total
        total += sum(nums[c_start:c_start + n_m])
        return (total, c_start + n_m)


def metadata_sum(nums):
    return metadata_sum_at(0, nums)[0]


# Part 2


def root_value_at(i, nums):
    n_c = nums[i]
    n_m = nums[i + 1]
    if n_c == 0:
        m_start = i + 2
        m_end = m_start + n_m
        return (sum(nums[m_start:m_end]), m_end)
    else:
        c_start = i + 2
        c_totals = []
        for _ in range(n_c):
            c_total, c_start = root_value_at(c_start, nums)
            c_totals.append(c_total)
        metadata = nums[c_start:c_start + n_m]
        total = sum(
            c_totals[m - 1] for m in metadata if 0 < m <= len(c_totals))
        return (total, c_start + n_m)


def root_value(nums):
    return root_value_at(0, nums)[0]


if __name__ == '__main__':
    with open('./resources/day8.txt', 'r') as f:
        nums = map(int, f.read().split())
    print('Part 1: {}'.format(metadata_sum(nums)))
    print('Part 2: {}'.format(root_value(nums)))
