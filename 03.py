def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def isSymbol(char):
    return not char.isalnum() and char != "."


def findPosition(input, row, col):
    if not input[row][col].isdigit():
        return None
    start = col
    while input[row][start].isdigit():
        start -= 1
    end = col
    while input[row][end].isdigit():
        end += 1
    return (row, start + 1, end - 1)


def part1(input):
    numberPositions = set()
    for r in range(0, len(input)):
        for c in range(0, len(input[r]) - 1):
            if isSymbol(input[r][c]):
                for dir in directions:
                    pos = findPosition(input, r + dir[0], c + dir[1])
                    if pos:
                        numberPositions.add(pos)
    acc = 0
    for np in numberPositions:
        number = int(input[np[0]][np[1] : np[2] + 1])
        acc += number
    return acc


def part2(input):
    gearRatiosSum = 0
    for r in range(0, len(input)):
        for c in range(0, len(input[r]) - 1):
            if input[r][c] == "*":
                positions = set()
                for dir in directions:
                    pos = findPosition(input, r + dir[0], c + dir[1])
                    if pos:
                        positions.add(pos)
                if len(positions) == 2:
                    gearRatio = 1
                    for p in positions:
                        number = int(input[p[0]][p[1] : p[2] + 1])
                        gearRatio *= number
                    gearRatiosSum += gearRatio
    return gearRatiosSum


testInput = readInput("03_test.txt")
assert part1(testInput) == 4361
assert part2(testInput) == 467835

input = readInput("03.txt")
print(part1(input))
print(part2(input))
