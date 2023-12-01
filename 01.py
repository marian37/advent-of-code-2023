import re


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


def part1(input):
    numbers = []
    for line in input:
        digits = re.sub("\\D", "", line)
        numbers.append(int(digits[0] + digits[-1]))

    return sum(numbers)


def matchesNumber(text):
    numbers = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    for i in range(0, len(numbers)):
        if text.startswith(numbers[i]):
            return str(i)
    return ""


def processLine(line):
    lineNumbers = []
    for i in range(0, len(line)):
        if line[i].isdigit():
            lineNumbers.append(line[i])
        else:
            lineNumbers.append(matchesNumber(line[i : i + 5]))
    return "".join(lineNumbers)


def part2(input):
    input2 = map(processLine, input)
    return part1(input2)


testInput1 = readInput("01_test1.txt")
assert part1(testInput1) == 142

testInput2 = readInput("01_test2.txt")
assert part2(testInput2) == 281

input = readInput("01.txt")
print(part1(input))
print(part2(input))
