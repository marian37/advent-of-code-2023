def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def checkLines(pattern, start=1):
    for i in range(start, len(pattern)):
        m = True
        for j in range(i):
            if i + j >= len(pattern):
                return i
            if pattern[i - 1 - j] != pattern[i + j]:
                m = False
                break
        if m:
            return i
    return 0


def processPattern(pattern, all=False):
    result = []
    rows = checkLines(pattern)
    if rows:
        result.append((rows, 0))
    if not all and len(result):
        return result[0]
    rows = checkLines(pattern, rows + 1)
    if rows:
        result.append((rows, 0))
    transformedPattern = []
    for c in range(len(pattern[0])):
        transformedPattern.append([])
    for r in range(len(pattern)):
        for c in range(len(pattern[r])):
            transformedPattern[c].append(pattern[r][c])
    for c in range(len(pattern[0])):
        transformedPattern[c] = "".join(transformedPattern[c])
    cols = checkLines(transformedPattern)
    if cols:
        result.append((0, cols))
    if not all:
        return result[0]
    cols = checkLines(transformedPattern, cols + 1)
    if cols:
        result.append((0, cols))
    return result


def processSmudged(pattern):
    original = processPattern(pattern)
    for r in range(len(pattern)):
        for c in range(len(pattern[r])):
            if pattern[r][c] == ".":
                pattern[r] = pattern[r][:c] + "#" + pattern[r][c + 1 :]
                reflections = processPattern(pattern, True)
                for rows, cols in reflections:
                    if (rows, cols) == original:
                        continue
                    if rows and min(rows, len(pattern) - rows) >= abs(rows - r):
                        return rows, cols
                    if cols and min(cols, len(pattern[0]) - cols) >= abs(cols - c):
                        return rows, cols
                pattern[r] = pattern[r][:c] + "." + pattern[r][c + 1 :]
    return 0, 0


def part1(input):
    result = 0
    lastStart = 0
    for i in range(len(input)):
        if input[i] == "":
            pattern = input[lastStart:i]
            lastStart = i + 1
            rows, cols = processPattern(pattern)
            result += rows * 100 + cols
    rows, cols = processPattern(input[lastStart:])
    result += rows * 100 + cols
    return result


def part2(input):
    result = 0
    lastStart = 0
    for i in range(len(input)):
        if input[i] == "":
            pattern = input[lastStart:i]
            lastStart = i + 1
            rows, cols = processSmudged(pattern)
            result += rows * 100 + cols
    rows, cols = processSmudged(input[lastStart:])
    result += rows * 100 + cols
    return result


testInput = readInput("13_test.txt")
assert part1(testInput) == 405
assert part2(testInput) == 400

input = readInput("13.txt")
print(part1(input))
print(part2(input))
