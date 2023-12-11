from enum import Enum
from collections import deque


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


directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

nextClockwise = {
    Direction.NORTH: (-1, 1),
    Direction.EAST: (1, 1),
    Direction.SOUTH: (1, -1),
    Direction.WEST: (-1, -1),
}

nextClockwiseDirs = {
    ("J", Direction.NORTH): [Direction.EAST, Direction.SOUTH],
    ("7", Direction.WEST): [Direction.NORTH, Direction.EAST],
    ("F", Direction.SOUTH): [Direction.WEST, Direction.NORTH],
    ("L", Direction.EAST): [Direction.SOUTH, Direction.WEST],
}

nextAntiClockwise = {
    Direction.NORTH: (-1, -1),
    Direction.EAST: (-1, 1),
    Direction.SOUTH: (1, 1),
    Direction.WEST: (1, -1),
}

nextAntiClockwiseDirs = {
    ("J", Direction.WEST): [Direction.SOUTH, Direction.EAST],
    ("7", Direction.SOUTH): [Direction.EAST, Direction.NORTH],
    ("F", Direction.EAST): [Direction.NORTH, Direction.WEST],
    ("L", Direction.NORTH): [Direction.WEST, Direction.SOUTH],
}


neighbours = {
    "|": (Direction.NORTH, Direction.SOUTH),
    "-": (Direction.EAST, Direction.WEST),
    "L": (Direction.NORTH, Direction.EAST),
    "J": (Direction.NORTH, Direction.WEST),
    "7": (Direction.SOUTH, Direction.WEST),
    "F": (Direction.SOUTH, Direction.EAST),
}


def getStartAndPrepareDist(input):
    dist = []
    start = (0, 0)
    for r in range(len(input)):
        dist.append([])
        for c in range(len(input[r])):
            dist[r].append(-1)
            if input[r][c] == "S":
                dist[r][c] = 0
                start = (r, c)
    return start, dist


def bfs(input, start, dist):
    queue = deque()
    for dir in directions:
        dr, dc = dir.value
        r = start[0] + dr
        c = start[1] + dc
        symbol = input[r][c]
        if not symbol in neighbours:
            continue
        for n in neighbours[symbol]:
            if n.value == (-dr, 0) or n.value == (0, -dc):
                queue.append((r, c))
                dist[r][c] = 1

    maxDist = 0
    while len(queue) != 0:
        r, c = queue.popleft()
        symbol = input[r][c]
        if not symbol in neighbours:
            continue
        for n in neighbours[symbol]:
            nextR = r + n.value[0]
            nextC = c + n.value[1]
            if dist[nextR][nextC] == -1:
                newDist = dist[r][c] + 1
                dist[nextR][nextC] = newDist
                maxDist = max(maxDist, newDist)
                queue.append((nextR, nextC))

    return dist, maxDist


def floodFill(dist, current, dir, clockwise):
    filled = 0
    n = nextClockwise[dir] if clockwise else nextAntiClockwise[dir]
    nr = current[0] + n[0]
    nc = current[1] + n[1]
    if (
        nr >= 0
        and nr < len(dist)
        and nc >= 0
        and nc < len(dist[nr])
        and dist[nr][nc] == -1
    ):
        queue = deque()
        queue.append((nr, nc))
        dist[nr][nc] = -2
        filled += 1
        while len(queue) != 0:
            qr, qc = queue.popleft()
            for d in directions:
                dr, dc = d.value
                r = qr + dr
                c = qc + dc
                if (
                    r >= 0
                    and r < len(dist)
                    and c >= 0
                    and c < len(dist[r])
                    and dist[r][c] == -1
                ):
                    queue.append((r, c))
                    dist[r][c] = -2
                    filled += 1
    return dist, filled


def countFromTop(dist, start):
    r = 0
    c = start[1]
    count = 0
    while r < start[0]:
        if dist[r][c] != -1:
            count += 1
            while abs(dist[r][c] - dist[r + 1][c]) == 1:
                r += 1
        r += 1
    return count


def part1(input):
    start, dist = getStartAndPrepareDist(input)

    dist, maxDist = bfs(input, start, dist)

    return maxDist


def part2(input, startDir):
    start, dist = getStartAndPrepareDist(input)

    dist, maxDist = bfs(input, start, dist)

    enclosedTiles = 0
    queue = deque()
    count = countFromTop(dist, start)
    for dir in directions:
        dr, dc = dir.value
        r, c = start
        nr = r + dr
        nc = c + dc
        if dist[nr][nc] == dist[r][c] + 1:
            queue.append((nr, nc, bool(count % 2 != 0) != bool(dir == startDir)))

    while len(queue) != 0:
        r, c, clockwise = queue.popleft()
        symbol = input[r][c]
        for dir in neighbours[symbol]:
            dr, dc = dir.value
            nr = r + dr
            nc = c + dc
            if (
                nr >= 0
                and nr < len(dist)
                and nc >= 0
                and nc < len(dist[nr])
                and dist[nr][nc] == dist[r][c] + 1
            ):
                queue.append((nr, nc, clockwise))
                dist, tiles = floodFill(dist, (r, c), dir, clockwise)
                enclosedTiles += tiles
                if clockwise and (symbol, dir) in nextClockwiseDirs:
                    for d in nextClockwiseDirs[(symbol, dir)]:
                        dist, tiles = floodFill(dist, (r, c), d, clockwise)
                        enclosedTiles += tiles
                if not clockwise and (symbol, dir) in nextAntiClockwiseDirs:
                    for d in nextAntiClockwiseDirs[(symbol, dir)]:
                        dist, tiles = floodFill(dist, (r, c), d, clockwise)
                        enclosedTiles += tiles

    return enclosedTiles


testInput1 = readInput("10_test1.txt")
testInput2 = readInput("10_test2.txt")
assert part1(testInput1) == 4
assert part1(testInput2) == 8

testInput3 = readInput("10_test3.txt")
testInput4 = readInput("10_test4.txt")
testInput5 = readInput("10_test5.txt")
testInput6 = readInput("10_test6.txt")

assert part2(testInput3, Direction.EAST) == 4
assert part2(testInput4, Direction.EAST) == 4
assert part2(testInput5, Direction.EAST) == 8
assert part2(testInput6, Direction.SOUTH) == 10

input = readInput("10.txt")
print(part1(input))
print(part2(input, Direction.SOUTH))
