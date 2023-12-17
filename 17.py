from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue


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


@dataclass(order=True)
class State:
    heat_loss: int
    data: (int, int, Direction, int) = field(compare=False)


def part1(input):
    shortest = {}
    queue = PriorityQueue()
    queue.put(State(int(input[0][1]), (0, 1, Direction.EAST, 0)))
    queue.put(State(int(input[1][0]), (1, 0, Direction.SOUTH, 0)))

    while not queue.empty():
        state = queue.get()
        heat_loss = state.heat_loss
        item = state.data
        r, c, dir, dir_count = item
        if r == len(input) - 1 and c == len(input[r]) - 1:
            return heat_loss
        dirId = directions.index(dir)
        for d in [0, 1, -1]:
            direction = directions[(dirId + d) % len(directions)]
            dr, dc = direction.value
            new_r = r + dr
            new_c = c + dc
            new_state_data = (new_r, new_c, direction, 0 if d != 0 else dir_count + 1)
            if (
                new_r >= 0
                and new_r < len(input)
                and new_c >= 0
                and new_c < len(input[0])
                and (d != 0 or dir_count < 2)
                and new_state_data not in shortest
            ):
                new_state = State(
                    heat_loss + int(input[new_r][new_c]),
                    new_state_data,
                )
                shortest.update({new_state_data: new_state.heat_loss})
                queue.put(new_state)
    return 0


def part2(input):
    shortest = {}
    queue = PriorityQueue()
    queue.put(State(int(input[0][1]), (0, 1, Direction.EAST, 0)))
    queue.put(State(int(input[1][0]), (1, 0, Direction.SOUTH, 0)))

    while not queue.empty():
        state = queue.get()
        heat_loss = state.heat_loss
        item = state.data
        r, c, dir, dir_count = item
        if r == len(input) - 1 and c == len(input[r]) - 1 and dir_count >= 3:
            return heat_loss
        dirId = directions.index(dir)
        for d in [0, 1, -1]:
            direction = directions[(dirId + d) % len(directions)]
            dr, dc = direction.value
            new_r = r + dr
            new_c = c + dc
            new_state_data = (new_r, new_c, direction, 0 if d != 0 else dir_count + 1)
            if (
                new_r >= 0
                and new_r < len(input)
                and new_c >= 0
                and new_c < len(input[0])
                and (d != 0 or dir_count < 9)
                and (d == 0 or dir_count >= 3)
                and new_state_data not in shortest
            ):
                new_state = State(
                    heat_loss + int(input[new_r][new_c]),
                    new_state_data,
                )
                shortest.update({new_state_data: new_state.heat_loss})
                queue.put(new_state)
    return 0


testInput = readInput("17_test.txt")
assert part1(testInput) == 102
assert part2(testInput) == 94
testInput2 = readInput("17_test2.txt")
assert part2(testInput2) == 71

input = readInput("17.txt")
print(part1(input))
print(part2(input))
