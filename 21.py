from enum import Enum


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


def find_start(input):
    start = (0, 0)
    for r in range(len(input)):
        for c in range(len(input[r])):
            if input[r][c] == "S":
                start = (r, c)
                break
    return start


def part1(input, steps):
    start = find_start(input)

    accessible = set()
    accessible.add(start)
    for i in range(steps):
        new_accessible = set()
        for a in accessible:
            ar, ac = a
            for d in Direction:
                dr, dc = d.value
                r = ar + dr
                c = ac + dc
                if (
                    r >= 0
                    and r < len(input)
                    and c >= 0
                    and c < len(input[r])
                    and input[r][c] != "#"
                ):
                    new_accessible.add((r, c))
        accessible = new_accessible

    return len(accessible)


def print_grouped_by_tiles(input, accessible, size):
    for i in range(-size, size + 1):
        for r in range(len(input)):
            for j in range(-size, size + 1):
                for c in range(len(input[r])):
                    value = input[r][c]
                    if value == "S" and (i != 0 or j != 0):
                        value = "."
                    nr = r + (i * len(input))
                    nc = c + (j * len(input[r]))
                    if (nr, nc) in accessible:
                        value = "O"
                    print(value, end="")
            print()


def group_by_tile(height, width, points):
    groups = {}
    for p in points:
        pr, pc = p
        r = pr // height
        c = pc // width
        if (r, c) in groups:
            groups[(r, c)].add(p)
        else:
            groups.update({(r, c): {p}})
    return groups


def part2(input, steps, real_input=False):
    start = find_start(input)

    accessible = set()
    accessible.add(start)
    values = []
    max_steps = 2 * len(input) + len(input) // 2 if real_input else steps
    for i in range(max_steps):
        new_accessible = set()
        for a in accessible:
            ar, ac = a
            for d in Direction:
                dr, dc = d.value
                r = ar + dr
                c = ac + dc
                mr = r % len(input)
                mc = c % len(input[mr])
                if input[mr][mc] != "#":
                    new_accessible.add((r, c))
        accessible = new_accessible
        if (i + 1 - len(input) // 2) % len(input) == 0:
            values.append(len(accessible))

    if not real_input:
        return len(accessible)

    c = values[0]
    for a in range(14000, 16000):
        b = values[1] - c - a
        if values[2] == a * 2 * 2 + b * 2 + c:
            break
    i = (steps - len(input) // 2) // len(input)
    return a * i * i + b * i + c


testInput = readInput("21_test.txt")
assert part1(testInput, 6) == 16

assert part2(testInput, 6) == 16
assert part2(testInput, 10) == 50
assert part2(testInput, 50) == 1594
assert part2(testInput, 100) == 6536
# assert part2(testInput, 500) == 167004
# assert part2(testInput, 1000) == 668697
# assert part2(testInput, 5000) == 16733044

input = readInput("21.txt")
print(part1(input, 64))
print(part2(input, 26501365, True))
