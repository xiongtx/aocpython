from itertools import cycle

def repeated_freq(freqs):
    current_freq = 0
    all_freqs = set([current_freq])
    for freq in cycle(freqs):
        current_freq += freq
        if current_freq in all_freqs:
            return current_freq
        else:
            all_freqs.add(current_freq)

if __name__ == '__main__':
    with open('./resources/day1.txt', 'r') as f:
        freqs = [int(n) for n in f.readlines()]
    print('Part 1: {}'.format(sum(freqs)))
    print('Part 2: {}'.format(repeated_freq(freqs)))
