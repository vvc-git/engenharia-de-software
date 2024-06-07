from __future__ import annotations
from os import listdir
from copy import deepcopy
from random import shuffle, seed

from card import Card, Suit

class Deck:
    def __init__(self) -> Deck:
        self.__files: list[str] = sorted(listdir("../img/"))
        self._cards: list[Card] = self.__make_main_deck()
        self._discard_pile: list[Card] = []
        shuffle(self._cards)

    def __make_test_deck(self) -> list[Card]:
        return [Card(11, Suit.DIAMONDS, self.__files[0], (120,174)) for i in range(20)]

    def __make_main_deck(self) -> list[Card]:
        cards = []

        for i in range(2):
            image_files = deepcopy(self.__files)
            size = (120,174)
            for number in range (1,14):
                cards.append(Card(number, Suit.CLUBS, image_files.pop(0), size))
                cards.append(Card(number, Suit.DIAMONDS, image_files.pop(0), size))
                cards.append(Card(number, Suit.HEARTS, image_files.pop(0), size))
                cards.append(Card(number, Suit.SPADES, image_files.pop(0), size))

        return cards

    def make_board_deck(self) -> list[Card]:
        cards = []

        for i in range(2):
            image_files = deepcopy(self.__files)
            size = (60,87)
            for number in range (1,14):
                cards.append(Card(number, Suit.CLUBS, image_files.pop(0), size))
                cards.append(Card(number, Suit.DIAMONDS, image_files.pop(0), size))
                cards.append(Card(number, Suit.HEARTS, image_files.pop(0), size))
                cards.append(Card(number, Suit.SPADES, image_files.pop(0), size))

            for i in range(2):
                cards.append(Card(0, Suit.JOKER, image_files[0], size))

            cards.remove(Card(11, Suit.CLUBS))
            cards.remove(Card(11, Suit.DIAMONDS))
            cards.remove(Card(11, Suit.HEARTS))
            cards.remove(Card(11, Suit.SPADES))

        shuffle(cards)
        return cards

    def draw(self) -> Card:
        if (self.deck_is_empty()):
            self.reshuffle()
        return self._cards.pop()

    def discard(self, card: Card):
        self._discard_pile.insert(0, card)

    def reshuffle(self):
        while len(self._discard_pile) > 0:
            self._cards.append(self._discard_pile.pop())
        shuffle(self._cards)

    def discard_pile_top(self) -> Card:
        return self._discard_pile[0] if len(self._discard_pile) else None

    def deck_is_empty(self) -> bool:
        return len(self._cards) == 0

    def discard_is_empty(self) -> bool:
        return len(self._discard_pile) == 0
