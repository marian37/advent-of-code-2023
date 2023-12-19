from dataclasses import dataclass
from enum import Enum
import re


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


@dataclass
class Rating:
    rating: dict
    x: int
    m: int
    a: int
    s: int

    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)
        self.rating = {"x": self.x, "m": self.m, "a": self.a, "s": self.s}

    @property
    def sum(self):
        return self.x + self.m + self.a + self.s


class Operation(Enum):
    GREATER = ">"
    LESS = "<"


class Condition:
    destination: str
    part: str
    operation: Operation
    value: int

    def __init__(self, destination, part=None, operation=None, value=None):
        self.destination = destination
        self.part = part
        self.operation = operation
        self.value = value

    def __str__(self) -> str:
        if self.operation:
            return f"({self.part}{self.operation.value}{self.value}:{self.destination})"
        return f"({self.destination})"

    def __repr__(self) -> str:
        return str(self)


def check(rating, condition):
    if condition.operation:
        if condition.operation == Operation.GREATER:
            return rating.rating[condition.part] > condition.value
        else:
            return rating.rating[condition.part] < condition.value
    else:
        return True


def parse_input(input):
    reg1 = re.compile("(?P<label>\\w+){(?P<workflow>\\S+)}")
    reg2 = re.compile("{x=(?P<x>\\d+),m=(?P<m>\\d+),a=(?P<a>\\d+),s=(?P<s>\\d+)}")
    read_ratings = False
    ratings = []
    workflows = {}
    for line in input:
        if line == "":
            read_ratings = True
            continue
        if read_ratings:
            m = reg2.match(line)
            rating = Rating(m.group("x"), m.group("m"), m.group("a"), m.group("s"))
            ratings.append(rating)
        else:
            m = reg1.match(line)
            label = m.group("label")
            workflow_desc = m.group("workflow")
            workflow = []
            for w in workflow_desc.split(","):
                w2 = w.split(":")
                if len(w2) == 1:
                    c = Condition(w2[0])
                else:
                    c = Condition(
                        w2[1],
                        w2[0][0],
                        Operation.GREATER if w2[0][1] == ">" else Operation.LESS,
                        int(w2[0][2:]),
                    )
                workflow.append(c)
            workflows.update({label: workflow})
    return workflows, ratings


def part1(input):
    workflows, ratings = parse_input(input)
    accepted = []
    for r in ratings:
        w = "in"
        while w != "A" and w != "R":
            workflow = workflows[w]
            for c in workflow:
                if check(r, c):
                    w = c.destination
                    break
        if w == "A":
            accepted.append(r)
    return sum([r.sum for r in accepted])


def size(interval):
    start, end = interval
    if end < start:
        return 0
    return end - start + 1


def split_intervals(rating_intervals, condition):
    i1 = {}
    i2 = {}
    for r in rating_intervals:
        if r == condition.part:
            r1, r2 = rating_intervals[r]
            if condition.operation == Operation.GREATER:
                i1.update({r: (condition.value + 1, r2)})
                i2.update({r: (r1, condition.value)})
            else:
                i1.update({r: (r1, condition.value - 1)})
                i2.update({r: (condition.value, r2)})
        else:
            i1.update({r: rating_intervals[r]})
            i2.update({r: rating_intervals[r]})
    return i1, i2


def count_accepted(workflows, rating_intervals, current):
    if current == "A":
        count = 1
        for k in rating_intervals:
            count *= size(rating_intervals[k])
        return count
    if current == "R":
        return 0
    current_workflow = workflows[current]
    count = 0
    for c in current_workflow:
        if c.operation:
            i1, i2 = split_intervals(rating_intervals, c)
            count += count_accepted(workflows, i1, c.destination)
            rating_intervals = i2
        else:
            count += count_accepted(workflows, rating_intervals, c.destination)
    return count


def part2(input):
    workflows, ratings = parse_input(input)
    current = "in"
    rating_intervals = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    return count_accepted(workflows, rating_intervals, current)


testInput = readInput("19_test.txt")
assert part1(testInput) == 19114
assert part2(testInput) == 167409079868000

input = readInput("19.txt")
print(part1(input))
print(part2(input))
