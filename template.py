def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def part1(input):
    return len(input)


def part2(input):
    return len(input)


testInput = readInput("00_test.txt")
assert part1(testInput) == 1
assert part2(testInput) == 1

input = readInput("00.txt")
print(part1(input))
print(part2(input))
