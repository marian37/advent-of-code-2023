from collections import deque
from dataclasses import dataclass


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


@dataclass
class Point3D:
    x: int
    y: int
    z: int

    def __sub__(self, other):
        if type(other) is Point3D:
            x = self.x + 1 - other.x
            y = self.y + 1 - other.y
            z = self.z + 1 - other.z
            return Point3D(x, y, z)
        return self


@dataclass
class Brick:
    id: int
    start: Point3D
    end: Point3D

    @property
    def direction(self):
        return self.end - self.start


def parse_input(input):
    bricks = []
    for i, line in enumerate(input):
        start, end = line.split("~")
        sx, sy, sz = start.split(",")
        ex, ey, ez = end.split(",")
        b = Brick(
            i, Point3D(int(sx), int(sy), int(sz)), Point3D(int(ex), int(ey), int(ez))
        )
        bricks.append(b)
    return bricks


def calc_supported_by(sorted_bricks):
    max_x = max([b.end.x for b in sorted_bricks])
    max_y = max([b.end.y for b in sorted_bricks])

    new_heights = {}
    supported_by = {}
    top_brick = []
    for y in range(max_y + 1):
        top_brick.append([])
        for x in range(max_x + 1):
            top_brick[y].append([])

    for brick in sorted_bricks:
        height = 1 + brick.direction.z
        sup = set()
        for y in range(brick.start.y, brick.end.y + 1):
            for x in range(brick.start.x, brick.end.x + 1):
                if len(top_brick[y][x]):
                    s = top_brick[y][x][-1]
                    top = new_heights[s] + brick.direction.z
                else:
                    top = 0
                if top == height:
                    sup.add(s)
                if top > height:
                    sup = {s}
                    height = top
                top_brick[y][x].append(brick.id)
        new_heights.update({brick.id: height})
        supported_by.update({brick.id: sup})
    return supported_by


def part1(input):
    bricks = parse_input(input)
    sorted_bricks = sorted(bricks, key=lambda brick: brick.start.z)

    supported_by = calc_supported_by(sorted_bricks)

    result = 0
    for brick in sorted_bricks:
        for s in supported_by:
            if len(supported_by[s]) == 1 and brick.id in supported_by[s]:
                break
        else:
            result += 1

    return result


def count_falling(supported_by, supports, brick):
    queue = deque()
    queue.append(brick)
    disintegrated = set()
    disintegrated.add(brick)
    while len(queue):
        current = queue.popleft()
        for s in supports[current]:
            diff = supported_by[s].difference(disintegrated)
            if len(diff) == 0:
                disintegrated.add(s)
                queue.append(s)
    return len(disintegrated) - 1


def part2(input):
    bricks = parse_input(input)
    sorted_bricks = sorted(bricks, key=lambda brick: brick.start.z)

    supported_by = calc_supported_by(sorted_bricks)
    supports = {}
    for brick in sorted_bricks:
        supports.update({brick.id: []})
        for s in supported_by:
            if brick.id in supported_by[s]:
                supports[brick.id].append(s)

    result = 0
    for brick in sorted_bricks:
        result += count_falling(supported_by, supports, brick.id)

    return result


testInput = readInput("22_test.txt")
assert part1(testInput) == 5
assert part2(testInput) == 7

input = readInput("22.txt")
print(part1(input))
print(part2(input))
