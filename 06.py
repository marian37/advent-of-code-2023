def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


def part1(input):
    result = 1
    times = list(map(lambda t: int(t), input[0].split(":")[1].split()))
    distances = list(map(lambda d: int(d), input[1].split(":")[1].split()))
    for i in range(0, len(times)):
        count = 0
        time = times[i]
        for t in range(0, time):
            dist = t * (time - t)
            if dist > distances[i]:
                count += 1
        result *= count
    return result


def part2(input):
    time = int(input[0].split(":")[1].replace(" ", ""))
    distance = int(input[1].split(":")[1].replace(" ", ""))
    count = 0
    for t in range(0, time):
        dist = t * (time - t)
        if dist > distance:
            count += 1
    return count


testInput = readInput("06_test.txt")
assert part1(testInput) == 288
assert part2(testInput) == 71503

input = readInput("06.txt")
print(part1(input))
print(part2(input))
