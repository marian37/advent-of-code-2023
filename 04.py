def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


class Card:
    def __init__(self, id=0, winningNumbers=[], myNumbers=[], matchingCount=0):
        self.id = id
        self.winningNumbers = winningNumbers
        self.myNumbers = myNumbers
        self.matchingCount = matchingCount

    @staticmethod
    def parseFromString(id, line):
        start = line.find(":") + 1
        winning, my = line[start:].split("|")
        winningNumbers = list(
            map(
                lambda n: int(n),
                filter(lambda s: s.isnumeric(), winning.strip().split(" ")),
            )
        )
        myNumbers = list(
            map(
                lambda n: int(n), filter(lambda s: s.isnumeric(), my.strip().split(" "))
            )
        )
        count = 0
        for num in myNumbers:
            if num in winningNumbers:
                count += 1
        return Card(id, winningNumbers, myNumbers, count)


def part1(input):
    acc = 0
    id = 1
    cards = []
    for line in input:
        card = Card.parseFromString(id, line)
        cards.append(card)
        id += 1
        if card.matchingCount >= 1:
            acc += pow(2, card.matchingCount - 1)
    return acc


def part2(input):
    id = 1
    cards = []
    cardsCount = []

    for line in input:
        card = Card.parseFromString(id, line)
        cards.append(card)
        id += 1

    for card in cards:
        cardsCount.append(1)

    for i in range(0, len(cards)):
        card = cards[i]
        for j in range(i + 1, i + 1 + card.matchingCount):
            cardsCount[j] += cardsCount[i]

    return sum(cardsCount)


testInput = readInput("04_test.txt")
assert part1(testInput) == 13
assert part2(testInput) == 30

input = readInput("04.txt")
print(part1(input))
print(part2(input))
