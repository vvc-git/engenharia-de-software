from __future__ import annotations

from card import Card

class Player():
    def __init__(self, name: str, chip_color: str) -> Player:
        self._id: str = ""
        self._name: str = name
        self._hand: list[Card] = []
        self._chips_color: str = chip_color
        self._winner: bool = False
        self._sequences: int = 0

    def initialize(self, id: str, name: str):
        self._id = id
        self._name = name

    def reset(self):
        self._id = ""
        self._name = ""
        self._hand = []
        self._winner = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @property
    def hand(self) -> list[Card]:
        return self._hand

    @property
    def chips_color(self) -> str:
        return self._chips_color

    @property
    def turn(self) -> bool:
        return self._turn

    @property
    def sequences(self) -> int:
        return self._sequences

    def set_winner(self, value: bool):
        self._winner = value

    def add_sequences(self, n: int):
        self._sequences = self._sequences + n

    def draw(self, card: Card):
        self._hand.append(card)

    def play(self, index: int) -> Card:
        return self._hand.pop(index)
