def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


class RGB:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0

    def __str__(self) -> str:
        return str((self.red, self.green, self.blue))

    def __repr__(self) -> str:
        return str(self)


class Game:
    def __init__(self):
        self.id = 0
        self.sets = []

    def __str__(self) -> str:
        return f"{self.id}, {self.sets}"

    @staticmethod
    def parseFromString(line):
        game = Game()
        label, description = line.split(":")

        _, id = label.split(" ")
        game.id = int(id)

        setsDesc = description.strip().split(";")
        sets = []
        for s in setsDesc:
            rgb = RGB()
            w = s.split(",")
            for c in w:
                count, color = c.strip().split(" ")
                count = int(count)
                if color == "red":
                    rgb.red = count
                elif color == "blue":
                    rgb.blue = count
                else:
                    rgb.green = count
            sets.append(rgb)
        game.sets = sets
        return game

    #  only 12 red cubes, 13 green cubes, and 14 blue cubes
    def isPossible(self):
        return all(
            map(lambda s: s.red <= 12 and s.green <= 13 and s.blue <= 14, self.sets)
        )

    def calcPower(self):
        red = max(map(lambda s: s.red, self.sets))
        green = max(map(lambda s: s.green, self.sets))
        blue = max(map(lambda s: s.blue, self.sets))
        return red * green * blue


def part1(input):
    possibleIdsSum = 0
    for line in input:
        game = Game.parseFromString(line)
        if game.isPossible():
            possibleIdsSum += game.id
    return possibleIdsSum


def part2(input):
    powersSum = 0
    for line in input:
        game = Game.parseFromString(line)
        powersSum += game.calcPower()
    return powersSum


testInput = readInput("02_test.txt")
assert part1(testInput) == 8
assert part2(testInput) == 2286

input = readInput("02.txt")
print(part1(input))
print(part2(input))
