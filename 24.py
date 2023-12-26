from dataclasses import dataclass
from z3 import *


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


@dataclass
class Point2D:
    x: float
    y: float


@dataclass
class Point3D:
    x: float
    y: float
    z: float


@dataclass
class Hailstone:
    position: Point3D
    velocity: Point3D

    @property
    def function_params_2D(self):
        k = self.velocity.y / self.velocity.x
        q = -k * self.position.x + self.position.y
        return k, q

    def is_in_future(self, intersection) -> bool:
        if self.velocity.x > 0:
            return intersection[0] > self.position.x
        return intersection[0] < self.position.x


def find_intersection_2D(stone_a, stone_b):
    ka, qa = stone_a.function_params_2D
    kb, qb = stone_b.function_params_2D

    if kb == ka:
        return None

    x = (qa - qb) / (kb - ka)
    y = ka * x + qa
    return x, y


def is_in_interval(point, interval) -> bool:
    px, py = point
    i_min, i_max = interval
    return px >= i_min and px <= i_max and py >= i_min and py <= i_max


def parse_input(input):
    hailstones = []
    for line in input:
        pos, vel = line.split("@")
        px, py, pz = pos.split(", ")
        position = Point3D(int(px), int(py), int(pz))
        vx, vy, vz = vel.split(", ")
        velocity = Point3D(int(vx), int(vy), int(vz))
        stone = Hailstone(position, velocity)
        hailstones.append(stone)
    return hailstones


def part1(input, interval):
    intersection_count = 0
    hailstones = parse_input(input)
    for i, ha in enumerate(hailstones):
        for j in range(i + 1, len(hailstones)):
            hb = hailstones[j]
            intersection = find_intersection_2D(ha, hb)
            if (
                intersection
                and ha.is_in_future(intersection)
                and hb.is_in_future(intersection)
                and is_in_interval(intersection, interval)
            ):
                intersection_count += 1
    return intersection_count


def part2(input):
    hailstones = parse_input(input)
    solver = Solver()
    x = Int("x")
    y = Int("y")
    z = Int("z")
    r = Int("r")
    s = Int("s")
    t = Int("t")
    u = Int("u")
    v = Int("v")
    w = Int("w")
    params = [r, s, t]
    for i, h in enumerate(hailstones[:3]):
        solver.add(x + params[i] * u == h.position.x + h.velocity.x * params[i])
        solver.add(y + params[i] * v == h.position.y + h.velocity.y * params[i])
        solver.add(z + params[i] * w == h.position.z + h.velocity.z * params[i])
    solver.check()
    result = solver.model()
    return result[x].as_long() + result[y].as_long() + result[z].as_long()


testInput = readInput("24_test.txt")
assert part1(testInput, (7, 27)) == 2
assert part2(testInput) == 47

input = readInput("24.txt")
print(part1(input, (200000000000000, 400000000000000)))
print(part2(input))
