from __future__ import annotations
from typing import TYPE_CHECKING

from player import Player
from card import Card

class BoardPlace():
    def __init__(self, card: Card):
        self._card: Card = card
        self._player_in_place: Player = None
        self._in_sequence: bool = False

    @property
    def card(self) -> Card:
        return self._card

    @property
    def player_in_place(self) -> Player:
        return self._player_in_place

    @property
    def in_sequence(self) -> bool:
        return self._in_sequence

    @in_sequence.setter
    def in_sequence(self, value: bool):
        self._in_sequence = value

    def empty(self):
        return self._player_in_place is None

    def put_chip(self, player: Player):
        self._player_in_place = player

    def take_chip(self):
        self._player_in_place = None
