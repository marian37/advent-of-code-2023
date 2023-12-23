from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import cache


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)


slopes = {
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
}


@dataclass
class Point2D:
    y: int
    x: int

    def __add__(self, other):
        if type(other) is Direction:
            return Point2D(self.y + other.value[0], self.x + other.value[1])
        return self

    def __eq__(self, __value: object) -> bool:
        if type(__value) is Point2D:
            return self.x == __value.x and self.y == __value.y
        return False

    def __hash__(self) -> int:
        return (self.y, self.x).__hash__()


def part1(input):
    stack = []
    distance = [[-1 for c in input[0]] for r in input]
    start = Point2D(0, input[0].index("."))
    end = Point2D(len(input) - 1, input[-1].index("."))
    distance[start.y][start.x] = 0
    stack.append(start)
    max_distance = 0
    while len(stack):
        current = stack.pop()
        if current == end:
            dist = distance[current.y][current.x]
            max_distance = max(max_distance, dist)
            continue
        for dir in Direction:
            n = current + dir
            if (
                n.y >= 0
                and input[n.y][n.x] != "#"
                and (
                    distance[n.y][n.x] == -1
                    or distance[current.y][current.x] - distance[n.y][n.x] > 1
                )
            ):
                symbol = input[n.y][n.x]
                if symbol in slopes:
                    direction = slopes[symbol]
                    if dir != direction:
                        continue
                distance[n.y][n.x] = distance[current.y][current.x] + 1
                stack.append(n)

    return max_distance


def find_next(input, distance, start, start_dir, end):
    queue = deque()
    distance[start.y][start.x] = 0
    first = start + start_dir
    if input[first.y][first.x] == "#" or distance[first.y][first.x] != -1:
        return None, 0
    distance[first.y][first.x] = 1
    queue.append(first)
    while len(queue):
        current = queue.pop()
        if current == end:
            dist = distance[current.y][current.x]
            distance[current.y][current.x] = 0
            return current, dist
        neighbours = [current + dir for dir in Direction]
        wall_neighbours = [input[n.y][n.x] for n in neighbours].count("#")
        if wall_neighbours < 2:
            dist = distance[current.y][current.x]
            distance[current.y][current.x] = 0
            return current, dist
        for n in neighbours:
            if input[n.y][n.x] != "#" and distance[n.y][n.x] < 1 and n != start:
                distance[n.y][n.x] = distance[current.y][current.x] + 1
                queue.append(n)
    return None, 0


graph: dict
graph_vertices: list


@cache
def longest(start, end, used):
    max_dist = -1000
    neighbours = graph[start]
    for n in neighbours:
        id = graph_vertices.index(n)
        if 1 << id & used:
            continue
        if n == end:
            max_dist = max(max_dist, neighbours[n])
        else:
            new_used = used | 1 << id
            max_dist = max(max_dist, neighbours[n] + longest(n, end, new_used))
    return max_dist


def part2(input):
    vertices = set()
    unhandled_vertices = set()
    edges = {}

    start = Point2D(0, input[0].index("."))
    end = Point2D(len(input) - 1, input[-1].index("."))

    distance = [[-1 for c in input[0]] for r in input]
    distance[start.y][start.x] = 0

    unhandled_vertices.add(start)
    while len(unhandled_vertices):
        current = unhandled_vertices.pop()
        if current == end:
            vertices.add(current)
            continue
        for dir in Direction:
            if current == start and dir != Direction.DOWN:
                continue
            next, dist = find_next(input, distance, current, dir, end)
            if next:
                if next not in vertices:
                    unhandled_vertices.add(next)
                if current in edges:
                    edges[current].update({next: dist})
                else:
                    edges.update({current: {next: dist}})
                if next in edges:
                    edges[next].update({current: dist})
                else:
                    edges.update({next: {current: dist}})
        vertices.add(current)

    global graph, graph_vertices
    graph = edges
    graph_vertices = list(vertices)
    used = 1 << graph_vertices.index(start)
    return longest(start, end, used)


testInput = readInput("23_test.txt")
assert part1(testInput) == 94
assert part2(testInput) == 154

input = readInput("23.txt")
print(part1(input))
print(part2(input))
