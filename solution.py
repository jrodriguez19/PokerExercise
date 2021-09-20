RANKING = {
    "HighCard": 1,
    "Pair": 2,
    "TwoPairs": 3,
    "Trio": 4,
    "Straight": 5,
    "Flush": 6,
    "FullHouse": 7,
    "Quad": 8,
    "StraightFlush": 9,
    "RoyalFlush": 10,
}


class Card:
    FACECARDS = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

    def __init__(self, number, suit) -> None:
        if number in Card.FACECARDS:
            self._number = Card.FACECARDS[number]
        else:
            self._number = int(number)
        self._suit = suit

    def getNumber(self):
        return self._number

    def getSuit(self):
        return self._suit

    def getValue(self):
        return [self._number, self._suit]


class Hand:
    def __init__(self, handList) -> None:
        xx = []
        for rawCard in handList:
            xx.append(Card(rawCard[0], rawCard[1]))
        self._hand = sorted(xx, key=lambda card: card.getNumber())

    def getAmountCards(self):
        return len(self._hand)

    def getCards(self):
        return list(map(lambda card: card.getValue(), self._hand))

    def getNumbers(self):
        return list(map(lambda card: card.getNumber(), self._hand))

    def getSuits(self):
        return list(map(lambda card: card.getSuit(), self._hand))


class HighCard:
    @staticmethod
    def check(hand):
        return ["HighCard", hand.getCards()[-1][0]]


class Pair:
    @staticmethod
    def check(hand):
        repeats = Repeats.getRepeats(hand)
        if len(repeats) == 1:
            if repeats[0][1] == 2:
                return ["Pair", repeats[0][0], HighCard.check(hand)[1]]
            else:
                return [False]
        else:
            return [False]


class TwoPairs:
    @staticmethod
    def check(hand):
        repeats = Repeats.getRepeats(hand)
        if len(repeats) == 2:
            if repeats[0][1] == 2 and repeats[1][1] == 2:
                return [
                    "TwoPairs",
                    repeats[0][0],
                    repeats[1][0],
                    HighCard.check(hand)[1],
                ]
            else:
                return [False]

        else:
            return [False]


class Trio:
    @staticmethod
    def check(hand):
        repeats = Repeats.getRepeats(hand)
        if len(repeats) == 1:
            if repeats[0][1] == 3:
                return ["Trio", repeats[0][0], HighCard.check(hand)[1]]
            else:
                return [False]

        else:
            return [False]


class Straight:
    @staticmethod
    def check(hand):
        for i, card in enumerate(hand.getCards(), hand.getCards()[0][0]):
            if i != card[0]:
                return [False]

        return ["Straight"]


class Flush:
    @staticmethod
    def check(hand):
        suits = set(map(lambda card: card[1], hand.getCards()))
        if len(suits) == 1:
            return ["Flush"]
        else:
            return [False]


class FullHouse:
    @staticmethod
    def check(hand):
        repeats = Repeats.getRepeats(hand)
        if len(repeats) == 2:
            if (
                repeats[0][1] == 3
                and repeats[1][1] == 2
                or repeats[0][1] == 2
                and repeats[1][1] == 3
            ):
                return [
                    "FullHouse",
                    repeats[0][0],
                    repeats[1][0],
                    HighCard.check(hand)[1],
                ]
            else:
                return [False]

        else:
            return [False]


class Quad:
    @staticmethod
    def check(hand):
        repeats = Repeats.getRepeats(hand)
        if len(repeats) == 1:
            if repeats[0][1] == 4:
                return ["Quad", repeats[0][0], HighCard.check(hand)[1]]
            else:
                return [False]

        else:
            return [False]


class StraightFlush(Straight, Flush):
    @staticmethod
    def check(hand):
        if Straight.check(hand)[0] and Flush.check(hand)[0]:
            return ["StraightFlush", hand.getCards()[-1][0]]
        else:
            return [False]


class RoyalFlush(Flush):
    @staticmethod
    def check(hand):
        ROYALFLUSHNUMBERS = [10, 11, 12, 13, 14]
        for card in hand.getCards():
            number = card[0]
            if number in ROYALFLUSHNUMBERS:
                ROYALFLUSHNUMBERS.remove(number)
            else:
                return [False]

        if Flush.check(hand)[0]:
            return ["RoyalFlush"]


class Repeats:
    @staticmethod
    def getRepeats(hand):
        numbers = hand.getNumbers()
        uniqueNumbers = set(numbers)
        repeats = []
        for unique in uniqueNumbers:
            counts = numbers.count(unique)
            if counts > 1:
                repeats.append([unique, counts])
        return repeats


class Poker:
    def tiebreaker(self, resultHand1, resultHand2):
        # {"HighCard":1, "Pair":2, "TwoPairs":3 , "Trio":4, "Straight":5, "Flush":6, "FullHouse":7, "Quad":8, "StraightFlush":9, "RoyalFlush":10}
        # if resultHand1[0] == "RoyalFlush":
        #     return "XXX"
        if resultHand1[0] == "StraightFlush":
            return 1 if resultHand1[1] > resultHand2[1] else 2
        elif resultHand1[0] == "Quad":
            return 1 if resultHand1[1] > resultHand2[1] else 2
        elif resultHand1[0] == "FullHouse":
            return 1 if resultHand1[1] > resultHand2[1] else 2
        # elif resultHand1[0] == "Flush":
        #     return 1 if resultHand1[1] > resultHand2 [1] else 2
        elif resultHand1[0] == "Trio":
            return 1 if resultHand1[1] > resultHand2[1] else 2
        elif resultHand1[0] == "TwoPairs":
            return 1 if resultHand1[1] > resultHand2[1] else 2
        elif resultHand1[0] == "Pair":
            if resultHand1[1] > resultHand2[1]:
                return 1
            elif resultHand1[1] < resultHand2[1]:
                return 2
            else:
                if (
                    resultHand1[2] > resultHand2[2]
                ):  # hay que hacer una especie de recursion hasta encontrar el mayor de las cartas en caso de empate con la mayor carta.
                    return 1
                else:
                    return 2
        else:
            if resultHand1[1] > resultHand2[1]:
                return 1
            else:
                return 2

    def evaluateHands(self, hand1, hand2):
        resultHand1 = self.check(hand1)
        print("hand1: ", resultHand1)
        resultHand2 = self.check(hand2)
        print("hand2: ", resultHand2)

        if RANKING[resultHand1[0]] > RANKING[resultHand2[0]]:
            return 1
        elif RANKING[resultHand1[0]] < RANKING[resultHand2[0]]:
            return 2
        else:
            return self.tiebreaker(resultHand1, resultHand2)

    def check(self, hand):
        rank = RoyalFlush.check(hand)
        if rank[0]:
            return rank
        rank = StraightFlush.check(hand)
        if rank[0]:
            return rank
        rank = Quad.check(hand)
        if rank[0]:
            return rank
        rank = FullHouse.check(hand)
        if rank[0]:
            return rank
        rank = Flush.check(hand)
        if rank[0]:
            return rank
        rank = Straight.check(hand)
        if rank[0]:
            return rank
        rank = Trio.check(hand)
        if rank[0]:
            return rank
        rank = TwoPairs.check(hand)
        if rank[0]:
            return rank
        rank = Pair.check(hand)
        if rank[0]:
            return rank

        return HighCard.check(hand)


# card1 = Card('3','S')
# card2 = Card('3','S')
# card3 = Card('Q','H')
# card4 = Card('2','S')
# card5 = Card('3','D')


# hand1 = Hand([card1, card2, card3, card4, card5])


def loadRawInput():
    file = open("tests.txt", "r")
    # file = open('poker-hands.txt','r')
    rawInput = file.readlines()
    file.close()
    return rawInput


def rawHands(rawInput):
    rawHands = []
    for line in rawInput:
        rawHands.append(line.split())
    return rawHands


def hands(rawHands):

    return hands


rawInput = loadRawInput()
rHands = rawHands(rawInput)
print(rHands)


poker = Poker()

for hand in rHands:
    print("Winner: ", poker.evaluateHands(Hand(hand[0:5]), Hand(hand[5:10])))
