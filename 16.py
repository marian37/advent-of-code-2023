from enum import Enum
from collections import deque


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


class Direction(Enum):
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    NORTH = (-1, 0)


directions = [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]

backMirror = {
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.EAST,
    Direction.WEST: Direction.NORTH,
    Direction.NORTH: Direction.WEST,
}

forwardMirror = {
    Direction.EAST: Direction.NORTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.SOUTH,
    Direction.NORTH: Direction.EAST,
}


def countEnergized(input, startR, startC, startDir):
    visited = []
    for r in input:
        visited.append([0 for c in r])

    queue = deque()
    queue.append((startR, startC, startDir))
    visited[startR][startC] = 1 << directions.index(startDir)

    while len(queue):
        item = queue.popleft()
        r, c, to = item
        if input[r][c] == "\\":
            dir = [backMirror[to]]
        elif input[r][c] == "/":
            dir = [forwardMirror[to]]
        elif input[r][c] == "|" and (to == Direction.EAST or to == Direction.WEST):
            dir = [Direction.NORTH, Direction.SOUTH]
        elif input[r][c] == "-" and (to == Direction.NORTH or to == Direction.SOUTH):
            dir = [Direction.EAST, Direction.WEST]
        else:
            dir = [to]
        for d in dir:
            newR = r + d.value[0]
            newC = c + d.value[1]
            i = directions.index(d)
            if (
                newR >= 0
                and newR < len(input)
                and newC >= 0
                and newC < len(input[0])
                and not visited[newR][newC] & 1 << i
            ):
                queue.append((newR, newC, d))
                visited[newR][newC] |= 1 << i

    result = 0
    for r in visited:
        for c in r:
            if c:
                result += 1
    return result


def part1(input):
    return countEnergized(input, 0, 0, Direction.EAST)


def part2(input):
    maxEnergized = 0
    for c in range(len(input[0])):
        e = countEnergized(input, 0, c, Direction.SOUTH)
        maxEnergized = max(maxEnergized, e)
        e = countEnergized(input, len(input) - 1, c, Direction.NORTH)
        maxEnergized = max(maxEnergized, e)
    for r in range(len(input)):
        e = countEnergized(input, r, 0, Direction.EAST)
        maxEnergized = max(maxEnergized, e)
        e = countEnergized(input, r, len(input[0]) - 1, Direction.WEST)
        maxEnergized = max(maxEnergized, e)
    return maxEnergized


testInput = readInput("16_test.txt")
assert part1(testInput) == 46
assert part2(testInput) == 51

input = readInput("16.txt")
print(part1(input))
print(part2(input))
