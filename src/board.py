from __future__ import annotations
from enum import Enum
import random

from player import Player
from deck import Deck
from card import Card, Suit
from board_place import BoardPlace

class Status(Enum):
    STARTING = "starting"
    YOUR_TURN_CARD = "your_turn_card"
    YOUR_TURN_BOARD = "your_turn_board"
    OPPONENT_TURN = "opponent_turn"
    FINISHED = "finished"
    WITHDRAW = "withdraw"

class Board():
    def __init__(self) -> Board:
        self._deck: Deck = None
        self._local_player: Player = Player("Local", "red")
        self._remote_player: Player = Player("Remote", "blue")
        self._turn_player: Player = None
        self._board_places: list[BoardPlace] = []
        self._match_status: Status = Status.STARTING

    def __make_board_places(self) -> list[BoardPlace]:
        deck = self._deck.make_board_deck()
        return [BoardPlace(card) for card in deck]

    @property
    def deck(self) -> Deck:
        return self._deck

    @property
    def board_places(self) -> list[BoardPlace]:
        return self._board_places

    @property
    def local_player(self) -> Player:
        return self._local_player

    @property
    def remote_player(self) -> Player:
        return self._remote_player

    @property
    def turn_player(self) -> Player:
        return self._turn_player

    @property
    def match_status(self) -> Status:
        return self._match_status

    @match_status.setter
    def match_status(self, value: Status):
        self._match_status = value

    @turn_player.setter
    def turn_player(self, value: Player):
        self._turn_player = value

    def start_match(self, players: list, local_player_id: str) -> str:
        info = ""
        player1_name = players[0][0]
        player1_id = players[0][1]
        player1_order = players[0][2]

        player2_name = players[1][0]
        player2_id = players[1][1]

        self._local_player.reset()
        self._remote_player.reset()
        self._local_player.initialize(player1_id, player1_name)
        self._remote_player.initialize(player2_id, player2_name)

        seed = int(player1_id) + int(player2_id)
        random.seed(seed)

        self._deck = Deck()
        self._board_places = self.__make_board_places()

        if player1_order == "1":
            info = "Sua vez"
            self._match_status = Status.YOUR_TURN_CARD
            self._turn_player = self._local_player
            for i in range(7):
                self._local_player.draw(self._deck.draw())
                self._remote_player.draw(self._deck.draw())
        else:
            info = "Vez do\noponente"
            self._match_status = Status.OPPONENT_TURN
            self._turn_player = self._remote_player
            for i in range(7):
                self._remote_player.draw(self._deck.draw())
                self._local_player.draw(self._deck.draw())
        return info

    def reset_game(self):
        self._local_player.reset()
        self._remote_player.reset()
        self._deck = None
        self._board_places = []
        self._match_status = Status.STARTING

    def __is_dead_card(self, card: Card) -> bool:
        for place in self._board_places:
            if (place.card == card and place.empty()) or (card.is_two_eyes_jack() and place.empty()) or (card.is_one_eye_jack() and not place.empty() and place.player_in_place != self._turn_player):
                return False
        return True

    def receive_withdrawal_notification(self):
        self._match_status = Status.WITHDRAW

    def pick_card(self, index: int) -> (dict, str):
        move_to_send = {}
        info = ""
        move_to_send["hand_index"] = index
        move_to_send["match_status"] = "progress"

        card = self._turn_player.play(index)
        self._deck.discard(card)

        if not self.__is_dead_card(card):
            info = "Aguardando\njogada no\ntabuleiro"
            self._match_status = Status.YOUR_TURN_BOARD
        else:
            info = "Carta\nmorta"
            new_card = self._deck.draw()
            self._turn_player.draw(new_card)

        return (move_to_send, info)

    def __verify_card(self, card: Card, place: BoardPlace) -> bool:
        is_valid = False
        if place.empty():
            if card == place.card:
                is_valid = True
            elif card.is_two_eyes_jack():
                is_valid = place.card.suit != Suit.JOKER
            else:
                is_valid = False
        elif card.is_one_eye_jack():
            if self._turn_player != place.player_in_place:
                is_valid = not place.in_sequence
            else:
                is_valid = False
        return is_valid

    def select_board_place(self, index) -> (dict, str):
        move_to_send = {}
        info = ""
        card = self._deck.discard_pile_top()
        place = self._board_places[index]

        valid = self.__verify_card(card, place)
        if valid:
            info = "Turno do\noponente"
            move_to_send["board_index"] = index
            move_to_send["match_status"] = "next"

            if card.is_one_eye_jack():
                place.take_chip()
            else:
                place.put_chip(self._turn_player)
                finished = self.evaluate_match_finish(place)
                if finished:
                    info = "Vitória\n de " + self._turn_player.name
                    self._turn_player.set_winner(True)
                    move_to_send["match_status"] = "finished"
                    self._match_status = Status.FINISHED
                else:
                    self._match_status = Status.OPPONENT_TURN
            new_card = self._deck.draw()
            self._turn_player.draw(new_card)
        else:
            info = "Local\ninválido"
        return (move_to_send, info)

    def receive_move(self, move: dict) -> str:
        info = ""
        if move["match_status"] == "progress":
            print("jogada da mão")
            self._turn_player = self._remote_player
            self.match_status = Status.OPPONENT_TURN
            hand_index = move["hand_index"]
            self.pick_card(hand_index)
            info = "Turno do\noponente"
        else:
            print("jogada no board")
            board_index = move["board_index"]
            self.select_board_place(board_index)

            if self._match_status != Status.FINISHED:
                self._turn_player = self._local_player
                info = "Sua vez"
                self._match_status = Status.YOUR_TURN_CARD
            else:
                info = "Vitória\n de " + self._turn_player.name
        return info

    def evaluate_match_finish(self, place: BoardPlace) -> bool:
        self._turn_player.add_sequences(self.check_sequence_line(place))
        self._turn_player.add_sequences(self.check_sequence_column(place))
        self._turn_player.add_sequences(self.check_sequence_diagonal(place))

        print(self._turn_player.name + " tem " + str(self._turn_player.sequences) + " sequencias")
        finished = self._turn_player.sequences >= 5

        return finished

    def check_sequence_line(self, place: BoardPlace) -> bool:
        chips_in_seq = 1

        idx = self.board_places.index(place)
        lim = self.find_line(idx)


        m1 = max(idx - 4, lim[0])
        m2 = min(idx + 4, lim[1])

        cond1 = self.has_sequence(list(range(lim[0], lim[1])))

        if cond1:
            return self.check_all_line_sequence(lim)

        else:
            # Verifying on left
            for l in range(idx - 1, m1 - 1, -1):
                if (self.board_places[l]._player_in_place == place._player_in_place) or self.board_places[l].card.suit == Suit.JOKER:
                    chips_in_seq += 1
                else:
                    break


            # Verifying on right
            m2 = min(idx + 4, lim[1])
            for r in range(idx + 1, m2 + 1):
                if (self.board_places[r].player_in_place == place.player_in_place) or self.board_places[r].card.suit == Suit.JOKER:
                    chips_in_seq += 1
                else:
                    break



        # Set in_sequence to True
        if chips_in_seq >= 5:
            for i in range(lim[0], lim[1] + 1):
                self.board_places[i].in_sequence = True
            return True

        return False

    def check_sequence_column(self, place: BoardPlace) -> bool:
        chips_in_seq = 1

        idx = self.board_places.index(place)
        lim = self.find_column(idx)

        # Verifying on top
        m1 = max(idx - 40, lim[0])
        m2 = min(idx + 40, lim[1])

        cond1 = self.has_sequence(list(range(lim[0], lim[1], 10)))

        if cond1:
            return self.check_all_column_sequence(lim)

        else:
            for l in range(idx - 10, m1 - 10, -10):
                if (self.board_places[l]._player_in_place == place._player_in_place) or self.board_places[l].card.suit == Suit.JOKER:
                    chips_in_seq += 1
                else:
                    break

            for r in range(idx + 10, m2 + 10, 10):
                if (self.board_places[r].player_in_place == place.player_in_place) or self.board_places[r].card.suit == Suit.JOKER:
                    chips_in_seq += 1
                else:
                    break

        # Set in_sequence to True
        if chips_in_seq >= 5:
            for i in range(lim[0], lim[1] + 10, 10):
                self.board_places[i].in_sequence = True
            return True

        return False

    def check_sequence_diagonal(self, place: BoardPlace) -> int:
        chips_in_seq1 = 1
        chips_in_seq2 = 1
        # Save the bounded elements in the diagonal to set in_sequence as true
        aux1 = -1
        aux2 = -1
        aux3 = -1
        aux4 = -1

        idx = self.board_places.index(place)
        digDC, digEB, digEC, digDB = self.find_diagonal(idx)

        # Verificar a sequencia na diagonal toda
        # Se o jogador ja tiver uma sequencia nessa diagonal, entao a unica forma de ter outra sequencia eh se todas as posicoes dessa diagonal tiver
        # sido ocupadas por esse jogador

        if self.has_sequence(digEC + [idx] + digDB):
            if self.check_sequence_in_all(digEC + [idx] + digDB):
                aux1 = digEC[-1]
                aux2 = digDB[-1]

        if self.has_sequence(digDC + [idx] + digEB):
            if self.check_sequence_in_all(digDC + [idx] + digEB):
                aux3 = digDC[-1]
                aux4 = digEB[-1]

        else:
            # Verificar sequencia na diagonal 1
            for i in digDC:
                if (self.board_places[i].player_in_place == self.turn_player) or  self.board_places[i].card.suit == Suit.JOKER:
                    chips_in_seq1 += 1
                    aux1 = i
                else:
                    break
            for i in digEB:
                if (self.board_places[i].player_in_place == self.turn_player) or  self.board_places[i].card.suit == Suit.JOKER:
                    chips_in_seq1 += 1
                    aux2 = i
                else:
                    break

            # Verificar sequencia na diagonal 2
            for i in digEC:
                if self.board_places[i].player_in_place == self.turn_player or self.board_places[i].card.suit == Suit.JOKER:
                    chips_in_seq2 += 1
                    aux3 = i
                else:
                    break
            for i in digDB:
                if self.board_places[i].player_in_place == self.turn_player or self.board_places[i].card.suit == Suit.JOKER:
                    chips_in_seq2 += 1
                    aux4 = i
                else:
                    break

        # Set in_sequence to True
        if (chips_in_seq1 > 4):
            print("Auxiliares: ", aux1, aux2)
            if aux1 == -1:
                aux1 = idx
            if aux2 == -1:
                aux2 = idx
            for i in range(aux1, aux2 + 9, 9):
                print("i1 do diagonal", i)
                if self.board_places[i].card.suit != Suit.JOKER:
                    self.board_places[i].in_sequence = True
        if (chips_in_seq2 > 4):
            if aux3 == -1:
                aux3 = idx
            if aux4 == -1:
                aux4 = idx
            for i in range(aux3, aux4 + 11, 11):
                print("i2 do diagonal", i)
                if self.board_places[i].card.suit != Suit.JOKER:
                    self.board_places[i].in_sequence = True

        return (chips_in_seq1 > 4) + (chips_in_seq2 > 4)



    def find_line(self, idx: int) -> tuple[int, int]:
        limite_sup_linha = idx
        limite_inf_linha = idx
        while (limite_sup_linha % 10) != 9:
            limite_sup_linha += 1
        while (limite_inf_linha % 10) != 0:
            limite_inf_linha -= 1
        return (limite_inf_linha, limite_sup_linha)

    def find_column(self, idx: int) -> tuple[int, int]:
        for i in range(0, 10):
            if (idx % 10) == i:
                limite_inf_col = i

        for i in range(90, 100):
            if (idx % 10) == (i % 10):
                limite_sup_col = i

        return (limite_inf_col, limite_sup_col)


    def find_diagonal(self, idx: int):
        c1 = idx - 9
        c2 = idx + 9
        c3 = idx - 11
        c4 = idx + 11
        borda_sup = list(range(0, 10))
        borda_inf = list(range(90, 100))
        borda_esq = list(range(0, 100, 10))
        borda_dir = list(range(9, 109, 10))

        # Diagonal1: pela direita cima
        digDC = list()
        while c1 >= 0:
            digDC.append(c1)
            if c1 in (borda_dir + borda_sup):
                break
            c1 -= 9

        # Pela esquerda baixo
        digEB = list()
        while c2 < 100:
            digEB.append(c2)
            if c2 in (borda_esq + borda_inf):
                break
            c2 += 9

        # Diagonal 2: esquerda cima
        digEC = list()
        while c3 >= 0:
            digEC.append(c3)
            if c3 in (borda_esq + borda_sup):
                break
            c3 -= 11

        # Pela direita baixo
        digDB = list()
        while c4 < 100:
            digDB.append(c4)
            if c4 in (borda_dir + borda_inf):
                break
            c4 += 11

        return digDC, digEB, digEC, digDB


    def check_all_line_sequence(self, lim: tuple) -> bool:
        count = 0
        for i in range(lim[0], lim[1] + 1):
            if self.board_places[i].player_in_place == self.turn_player or  self.board_places[i].card.suit == Suit.JOKER:
                count += 1

        if count > 9:
            for i in range(lim[0], lim[1] + 1):
                self.board_places[i].in_sequence = True
            return True

        else:
            return False

    def check_all_column_sequence(self, lim: tuple) -> bool:
        count = 0
        for i in range(lim[0], lim[1] + 10, 10):
            if self.board_places[i].player_in_place == self.turn_player or  self.board_places[i].card.suit == Suit.JOKER:
                count += 1

        if count > 9:
            for i in range(lim[0], lim[1] + 10, 10):
                self.board_places[i].in_sequence = True
            return True

        else:
            return False

    def has_sequence(self, l: list) -> bool:
        aux1 = 0
        for i in l:
            if self.board_places[i].in_sequence:
                aux1 += 1
            if aux1 > 4:
                return True

        return False

    def check_sequence_in_all(self, l: list) -> bool:
        count = 0
        for i in l:
            if self.board_places[i].player_in_place == self.turn_player or  self.board_places[i].card.suit == Suit.JOKER:
                count += 1

        if count > 9:
            return True

        else:
            return False
