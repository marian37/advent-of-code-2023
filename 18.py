from bisect import insort
from collections import deque
from enum import Enum
from itertools import batched, pairwise


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


class Point2D:
    x: int
    y: int

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other):
        if type(other) is Point2D:
            return Point2D(self.y + other.y, self.x + other.x)
        elif type(other) is int:
            return Point2D(self.y + other, self.x + other)
        else:
            return self

    def __mul__(self, other):
        if type(other) is int:
            return Point2D(other * self.y, other * self.x)
        return self

    def __rmul__(self, other):
        return self.__mul__(other)


class Direction(Enum):
    RIGHT = Point2D(0, 1)
    DOWN = Point2D(1, 0)
    LEFT = Point2D(0, -1)
    UP = Point2D(-1, 0)


directions = {
    "R": Direction.RIGHT,
    "D": Direction.DOWN,
    "L": Direction.LEFT,
    "U": Direction.UP,
}

color_directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]


def get_corners(input, part2=False):
    start = Point2D(0, 0)
    corners = [start]
    current = start
    for line in input[:-1]:
        direction, steps, color = line.split()
        if part2:
            d = color_directions[int(color[7])]
            s = int(color[2:7], 16)
        else:
            d = directions[direction]
            s = int(steps)
        current = current + (s * d.value)
        corners.append(current)

    x = [p.x for p in corners]
    y = [p.y for p in corners]
    min_x = min(x)
    offset_x = 0 - min_x
    min_y = min(y)
    offset_y = 0 - min_y

    offset = Point2D(offset_y, offset_x)
    corners = [c + offset for c in corners]

    return corners


def floodfill(plan, start):
    new_plan = []
    for r in plan:
        new_plan.append(r.copy())

    queue = deque()
    queue.append(start)
    new_plan[start.y][start.x] = "#"
    while len(queue):
        point = queue.popleft()
        for d in directions.values():
            n = point + d.value
            if (
                n.x >= 0
                and n.x < len(plan[0])
                and n.y >= 0
                and n.y < len(plan)
                and new_plan[n.y][n.x] != "#"
            ):
                new_plan[n.y][n.x] = "#"
                queue.append(n)

    return new_plan


def intersect(a1, a2, b1, b2):
    if b1 > a2 or a1 > b2:
        return 0
    o1 = max(a1, b1)
    o2 = min(a2, b2)
    return o2 - o1 + 1


def part1(input):
    corners = get_corners(input)

    x = [p.x for p in corners]
    y = [p.y for p in corners]
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)

    plan = [["." for c in range(min_x, max_x + 1)] for r in range(min_y, max_y + 1)]
    for a, b in pairwise(corners):
        if a.x == b.x:
            for i in range(min(a.y, b.y), max(a.y, b.y) + 1):
                plan[i][a.x] = "#"
        if a.y == b.y:
            for i in range(min(a.x, b.x), max(a.x, b.x) + 1):
                plan[a.y][i] = "#"

    filled_plan = floodfill(plan, Point2D(1, 1))

    result = 0
    for p in filled_plan:
        result += p.count("#")

    return result


def solve(input, part2=False):
    corners = get_corners(input, part2)
    c_map = {}
    for c in corners:
        if c.y in c_map:
            insort(c_map[c.y], c.x)
        else:
            c_map.update({c.y: [c.x]})

    sorted_keys = sorted(c_map.keys())
    result = 0
    active = []
    for j, k in enumerate(sorted_keys):
        if j != 0:
            for x1, x2 in batched(active, 2):
                size = (x2 - x1 + 1) * (k - sorted_keys[j - 1] + 1)
                result += size

        new_active = active.copy()
        for n in c_map[k]:
            if n in active:
                new_active.remove(n)
            else:
                insort(new_active, n)

        for a1, a2 in batched(active, 2):
            for b1, b2 in batched(new_active, 2):
                size = intersect(a1, a2, b1, b2)
                result -= size

        active = new_active

    return result


def part2(input):
    return len(input)


testInput = readInput("18_test.txt")
assert part1(testInput) == 62
assert solve(testInput, False) == 62
assert solve(testInput, True) == 952408144115

input = readInput("18.txt")
print(solve(input, False))
print(solve(input, True))
