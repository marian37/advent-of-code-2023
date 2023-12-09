import re
from itertools import cycle
from math import lcm


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


def part1(input):
    rl = input[0].strip()
    network = {}
    reg = re.compile("(?P<first>\\w+) = \\((?P<second>\\w+), (?P<third>\\w+)\\)")
    for line in input[2:]:
        m = reg.match(line)
        network[m.group("first")] = (m.group("second"), m.group("third"))
    count = 0
    current = "AAA"
    for d in cycle(rl):
        if current == "ZZZ":
            break
        current = network[current][1] if d == "R" else network[current][0]
        count += 1
    return count


def part2(input):
    rl = input[0].strip()
    network = {}
    reg = re.compile("(?P<first>\\w+) = \\((?P<second>\\w+), (?P<third>\\w+)\\)")
    for line in input[2:]:
        m = reg.match(line)
        network[m.group("first")] = (m.group("second"), m.group("third"))
    current = list(filter(lambda l: l[-1] == ("A"), network.keys()))
    periods = []
    for curr in current:
        c = curr
        count = 0
        for d in cycle(rl):
            if c[-1] == "Z":
                periods.append(count)
                break
            c = network[c][1] if d == "R" else network[c][0]
            count += 1
    return lcm(*periods)


testInput1 = readInput("08_test1.txt")
testInput2 = readInput("08_test2.txt")
assert part1(testInput1) == 2
assert part1(testInput2) == 6

testInput3 = readInput("08_test3.txt")
assert part2(testInput1) == 2
assert part2(testInput2) == 6
assert part2(testInput3) == 6

input = readInput("08.txt")
print(part1(input))
print(part2(input))
