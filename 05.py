from itertools import batched, starmap


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


class Almanac:
    def __init__(self):
        self.seeds = []
        self.maps = []

    @staticmethod
    def fromInput(input):
        almanac = Almanac()

        seedsLine = input[0]
        seedsLineStart = seedsLine.find(":")
        seeds = list(map(lambda n: int(n), seedsLine[seedsLineStart + 1 :].split()))
        almanac.seeds = seeds

        maps = []
        for line in input[2:]:
            if line[0].isdigit():
                maps[-1].append(tuple(map(lambda n: int(n), line.split())))
            elif line[0] == "\n":
                pass
            else:
                maps.append([])
        almanac.maps = maps

        return almanac


def processMap(seeds, map):
    newSeeds = []
    for seed in seeds:
        newSeed = seed
        for destStart, sourceStart, rangeLength in map:
            d = seed - sourceStart
            if d >= 0 and d < rangeLength:
                newSeed = destStart + d
                break
        newSeeds.append(newSeed)
    return newSeeds


def processMap2(seeds, map):
    newSeeds = list(starmap(lambda s, l: (s, s, l), seeds))
    for destStart, sourceStart, rangeLength in map:
        sourceEnd = sourceStart + rangeLength - 1
        s = newSeeds.copy()
        for destRangeStart, seedRangeStart, seedRangeLength in s:
            seedRangeEnd = seedRangeStart + seedRangeLength - 1
            if sourceStart <= seedRangeStart:
                if sourceEnd < seedRangeStart:
                    # no intersection
                    continue
                elif sourceEnd < seedRangeEnd:
                    # partial intersect
                    newSeeds.remove((destRangeStart, seedRangeStart, seedRangeLength))
                    l = sourceEnd - seedRangeStart + 1
                    newSeeds.append(
                        (seedRangeStart - sourceStart + destStart, seedRangeStart, l)
                    )
                    newSeeds.append(
                        (destRangeStart + l, sourceEnd + 1, seedRangeLength - l)
                    )
                else:
                    # parent interval
                    newSeeds.remove((destRangeStart, seedRangeStart, seedRangeLength))
                    newSeeds.append(
                        (
                            seedRangeStart - sourceStart + destStart,
                            seedRangeStart,
                            seedRangeLength,
                        )
                    )
            else:
                if sourceEnd <= seedRangeEnd:
                    # subinterval
                    newSeeds.remove((destRangeStart, seedRangeStart, seedRangeLength))
                    newSeeds.append(
                        (destRangeStart, seedRangeStart, sourceStart - seedRangeStart)
                    )
                    newSeeds.append((destStart, sourceStart, rangeLength))
                    newSeeds.append(
                        (
                            destRangeStart + sourceEnd - seedRangeStart,
                            sourceEnd + 1,
                            seedRangeEnd - sourceEnd,
                        )
                    )
                elif sourceStart <= seedRangeEnd:
                    # partial intersect
                    newSeeds.remove((destRangeStart, seedRangeStart, seedRangeLength))
                    l = seedRangeEnd - sourceStart + 1
                    newSeeds.append((destStart, sourceStart, l))
                    newSeeds.append(
                        (destRangeStart, seedRangeStart, seedRangeLength - l)
                    )
                else:
                    # no intersection
                    continue
    return list(starmap(lambda d, s, l: (d, l), newSeeds))


def part1(input):
    a = Almanac.fromInput(input)
    s = a.seeds
    for m in a.maps:
        s = processMap(s, m)
    return min(s)


def part2(input):
    a = Almanac.fromInput(input)
    s = list(batched(a.seeds, 2))
    for m in a.maps:
        s = processMap2(s, m)
    return min(starmap(lambda i, l: i, s))


testInput = readInput("05_test.txt")
assert part1(testInput) == 35
assert part2(testInput) == 46

input = readInput("05.txt")
print(part1(input))
print(part2(input))
