from functools import cache


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def replaceUnknown(text, i):
    replaced = []
    j = 0
    for c in text:
        if c == "?":
            bit = i & 1 << j
            if bit:
                replaced.append("#")
            else:
                replaced.append(".")
            j += 1
        else:
            replaced.append(c)
    return "".join(replaced)


def check(arrangement, numbers):
    j = 0
    count = 0
    for i in range(len(arrangement)):
        if arrangement[i] == "#":
            count += 1
        else:
            if count == 0:
                continue
            else:
                if j >= len(numbers) or count != numbers[j]:
                    return False
                else:
                    count = 0
                    j += 1
    if count == 0 and j < len(numbers):
        return False
    if count != 0 and (j != len(numbers) - 1 or count != numbers[j]):
        return False
    return True


def part1_backtrack(input):
    result = 0
    for line in input:
        text, numbersPart = line.split()
        numbers = list(map(int, numbersPart.split(",")))
        unknown = text.count("?")
        allPossible = 1 << unknown
        allowedArrangements = 0
        for i in range(allPossible):
            arrangement = replaceUnknown(text, i)
            isAllowed = check(arrangement, numbers)
            if isAllowed:
                allowedArrangements += 1
        result += allowedArrangements
    return result


@cache
def generateAndCheck(text, numbers, current, count):
    if current == len(text):
        if len(numbers) == 0:
            return 1
        return 0
    remainingText = text[current:]
    if len(numbers) == 0:
        if "#" in remainingText:
            return 0
        else:
            return 1
    if (
        len(numbers) == 1
        and len(remainingText) == numbers[0]
        and "." not in remainingText
        and count == 0
    ):
        return 1
    if count > numbers[0]:
        return 0
    if text[current] == "#":
        return generateAndCheck(text, numbers, current + 1, count + 1)
    elif text[current] == ".":
        if count:
            if count == numbers[0]:
                return generateAndCheck(text, numbers[1:], current + 1, 0)
            else:
                return 0
        else:
            return generateAndCheck(text, numbers, current + 1, count)
    else:
        if count:
            if count == numbers[0]:
                return generateAndCheck(text, numbers[1:], current + 1, 0)
            else:
                return generateAndCheck(text, numbers, current + 1, count + 1)
        else:
            return generateAndCheck(text, numbers, current + 1, 1) + generateAndCheck(
                text, numbers, current + 1, 0
            )


def part1_memoized(input):
    result = 0
    for line in input:
        text, numbersPart = line.split()
        numbers = list(map(int, numbersPart.split(",")))
        allowedArrangements = generateAndCheck(text, tuple(numbers), 0, 0)
        result += allowedArrangements
    return result


def mapLine(line):
    times = 5
    text, numbersPart = line.split()
    return f"{'?'.join([text for i in range(times)])} {','.join([numbersPart for i in range(times)])}"


def part2(input):
    return part1_memoized(list(map(mapLine, input)))


testInput = readInput("12_test.txt")
assert part1_backtrack(testInput) == 21
assert part1_memoized(testInput) == 21
assert part2(testInput) == 525152

input = readInput("12.txt")
print(part1_backtrack(input))
print(part1_memoized(input))
print(part2(input))
