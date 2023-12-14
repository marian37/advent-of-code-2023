def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def slideNorth(transformed):
    for r in range(len(transformed)):
        for c in range(len(transformed[r])):
            if transformed[r][c] == "O":
                newR = r - 1
                while newR >= 0 and transformed[newR][c] == ".":
                    newR -= 1
                newR += 1
                transformed[r][c] = "."
                transformed[newR][c] = "O"
    return transformed


def slideWest(transformed):
    for r in range(len(transformed)):
        for c in range(len(transformed[r])):
            if transformed[r][c] == "O":
                newC = c - 1
                while newC >= 0 and transformed[r][newC] == ".":
                    newC -= 1
                newC += 1
                transformed[r][c] = "."
                transformed[r][newC] = "O"
    return transformed


def slideSouth(transformed):
    for r in range(len(transformed) - 1, -1, -1):
        for c in range(len(transformed[r])):
            if transformed[r][c] == "O":
                newR = r + 1
                while newR < len(transformed) and transformed[newR][c] == ".":
                    newR += 1
                newR -= 1
                transformed[r][c] = "."
                transformed[newR][c] = "O"
    return transformed


def slideEast(transformed):
    for r in range(len(transformed)):
        for c in range(len(transformed[r]) - 1, -1, -1):
            if transformed[r][c] == "O":
                newC = c + 1
                while newC < len(transformed[r]) and transformed[r][newC] == ".":
                    newC += 1
                newC -= 1
                transformed[r][c] = "."
                transformed[r][newC] = "O"
    return transformed


def calculateNorthSupportBeams(transformed):
    result = 0
    for r in range(len(transformed)):
        c = transformed[r].count("O")
        result += c * (len(transformed) - r)
    return result


def checkPeriod(beams, period):
    return beams[-period:] == beams[-2 * period : -period]


def part1(input):
    t = []
    for r in range(len(input)):
        t.append([])
        for c in range(len(input[r])):
            t[-1].append(input[r][c])
    transformed = slideNorth(t)
    return calculateNorthSupportBeams(transformed)


def part2(input):
    t = []
    for r in range(len(input)):
        t.append([])
        for c in range(len(input[r])):
            t[-1].append(input[r][c])
    supportBeams = [calculateNorthSupportBeams(t)]
    m = supportBeams[0]
    i = 0
    c = 0
    period = 0
    while True:
        t = slideNorth(t)
        t = slideWest(t)
        t = slideSouth(t)
        t = slideEast(t)
        c += 1
        beams = calculateNorthSupportBeams(t)
        if beams < m:
            m = beams
            i = c
        elif beams == m and c - i > 5:
            period = c - i
            if checkPeriod(supportBeams, period):
                break
            m = beams
            i = c
        supportBeams.append(beams)
    index = (1000000000 - c) % period
    return supportBeams[-period:][index]


testInput = readInput("14_test.txt")
assert part1(testInput) == 136
assert part2(testInput) == 64

input = readInput("14.txt")
print(part1(input))
print(part2(input))
