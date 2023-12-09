from itertools import pairwise


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


def part1(input):
    result = 0
    for line in input:
        dataset = list(map(int, line.split()))
        seq = dataset
        last = [dataset[-1]]
        while not all(map(lambda n: n == 0, seq)):
            diffs = []
            for l, r in pairwise(seq):
                diffs.append(r - l)
            seq = diffs
            last.append(diffs[-1])
        n = 0
        for i in range(len(last) - 1, -1, -1):
            n += last[i]
        result += n
    return result


def part2(input):
    result = 0
    for line in input:
        dataset = list(map(int, line.split()))
        seq = dataset
        first = [dataset[0]]
        while not all(map(lambda n: n == 0, seq)):
            diffs = []
            for l, r in pairwise(seq):
                diffs.append(l - r)
            seq = diffs
            first.append(diffs[0])
        n = 0
        for i in range(len(first) - 1, -1, -1):
            n += first[i]
        result += n
    return result


testInput = readInput("09_test.txt")
assert part1(testInput) == 114
assert part2(testInput) == 2

input = readInput("09.txt")
print(part1(input))
print(part2(input))
