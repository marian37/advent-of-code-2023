from collections import deque


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.read().splitlines()
    file.close()
    return lines


def getHash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def part1(input):
    result = 0
    for line in input:
        sequence = line.split(",")
        for s in sequence:
            h = getHash(s)
            result += h
    return result


def addToHashmap(hashmap, hash, text, number):
    queue = hashmap[hash]
    for i, item in enumerate(queue):
        t, n = item
        if t == text:
            queue[i] = (text, number)
            return
    queue.append((text, number))


def removeFromHashmap(hashmap, hash, text):
    queue = hashmap[hash]
    toRemove = -1
    for i, item in enumerate(queue):
        t, n = item
        if t == text:
            toRemove = i
    if toRemove != -1:
        queue.remove(queue[toRemove])


def part2(input):
    hashmap = [deque() for i in range(256)]
    for line in input:
        sequence = line.split(",")
        for s in sequence:
            if s[-1] == "-":
                h = getHash(s[:-1])
                removeFromHashmap(hashmap, h, s[:-1])
            else:
                t, n = s.split("=")
                h = getHash(t)
                addToHashmap(hashmap, h, t, int(n))
    result = 0
    for i, queue in enumerate(hashmap):
        for j, item in enumerate(queue):
            t, n = item
            result += (i + 1) * (j + 1) * n
    return result


testInput = readInput("15_test.txt")
assert part1(testInput) == 1320
assert part2(testInput) == 145

input = readInput("15.txt")
print(part1(input))
print(part2(input))
