from __future__ import annotations
from PIL import Image, ImageTk
from enum import Enum

class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"
    JOKER = "joker"

class Card:
    def __init__(self, number: int, suit: Suit, image_path: str = "", size: tuple(int,int) = (0,0)) -> Card:
        self._number: int = number
        self._suit: Suit = suit
        if image_path != "":
            self._image: PhotoImage = ImageTk.PhotoImage(Image.open("../img/" + image_path).resize(size))

    @property
    def number(self) -> int:
        return self._number

    @property
    def suit(self) -> Suit:
        return self._suit

    @property
    def image(self) -> PhotoImage:
        return self._image

    def is_two_eyes_jack(self) -> bool:
        return self == Card(11, Suit.DIAMONDS) or self == Card(11, Suit.CLUBS)

    def is_one_eye_jack(self) -> bool:
        return self == Card(11, Suit.HEARTS) or self == Card(11, Suit.SPADES)

    def __eq__(self, other):
        return (self.number == other.number and self.suit == other.suit)
    def __ne__(self, other):
        return not self.__eq__(self, other)
