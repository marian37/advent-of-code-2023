from enum import IntEnum
from functools import total_ordering


def readInput(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    return lines


class Strength(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


cardValues = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def getCardValue(card, useJokers):
    if useJokers and card == "J":
        return 1
    return cardValues[card]


@total_ordering
class Hand:
    def __init__(self, cards, bid, useJokers=False):
        self.cards = cards
        self.bid = bid
        self.useJokers = useJokers
        self.strength = Hand.calculateStrength(cards, useJokers)

    def __str__(self) -> str:
        return f"{self.cards} {self.bid} {self.useJokers} {self.strength}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value) -> bool:
        return self.cards == __value.cards

    def __gt__(self, __value) -> bool:
        if self.strength > __value.strength:
            return True
        elif self.strength < __value.strength:
            return False
        else:
            for i in range(0, len(self.cards)):
                if getCardValue(self.cards[i], self.useJokers) > getCardValue(
                    __value.cards[i], self.useJokers
                ):
                    return True
                elif getCardValue(self.cards[i], self.useJokers) < getCardValue(
                    __value.cards[i], self.useJokers
                ):
                    return False
                else:
                    continue
            return False

    @staticmethod
    def calculateStrength(cards, useJokers):
        cardsCount = {}
        for c in cards:
            if c in cardsCount:
                cardsCount[c] = cardsCount[c] + 1
            else:
                cardsCount[c] = 1
        cardsMax = max(cardsCount.values())
        if useJokers:
            m = 0
            for c, v in cardsCount.items():
                if c != "J" and v > m:
                    m = v
            cardsMax = m + cardsCount["J"] if "J" in cardsCount else m
        strength = Strength.HIGH_CARD
        if cardsMax == 5:
            strength = Strength.FIVE_OF_A_KIND
        elif cardsMax == 4:
            strength = Strength.FOUR_OF_A_KIND
        elif cardsMax == 3:
            if useJokers and "J" in cardsCount:
                jokers = cardsCount["J"]
                if (
                    jokers == 1
                    and Hand.calculateStrength(cards, False) == Strength.TWO_PAIR
                ):
                    strength = Strength.FULL_HOUSE
                else:
                    strength = Strength.THREE_OF_A_KIND

            else:
                if 2 in cardsCount.values():
                    strength = Strength.FULL_HOUSE
                else:
                    strength = Strength.THREE_OF_A_KIND
        elif cardsMax == 2:
            if useJokers and "J" in cardsCount:
                strength = Strength.ONE_PAIR
            else:
                if list(cardsCount.values()).count(2) == 2:
                    strength = Strength.TWO_PAIR
                else:
                    strength = Strength.ONE_PAIR
        else:
            strength = Strength.HIGH_CARD

        return strength


def part1(input):
    hands = []
    for line in input:
        cards, bid = line.split()
        hand = Hand(cards, int(bid))
        hands.append(hand)
    hands.sort()
    result = 0
    for i in range(0, len(hands)):
        result += hands[i].bid * (i + 1)
    return result


def part2(input):
    hands = []
    for line in input:
        cards, bid = line.split()
        hand = Hand(cards, int(bid), True)
        hands.append(hand)
    hands.sort()
    result = 0
    for i in range(0, len(hands)):
        result += hands[i].bid * (i + 1)
    return result


testInput = readInput("07_test.txt")
assert part1(testInput) == 6440
assert part2(testInput) == 5905

input = readInput("07.txt")
print(part1(input))
print(part2(input))
