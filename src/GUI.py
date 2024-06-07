from __future__ import annotations
from itertools import zip_longest

from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

from board import Board, Status
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

class GUI(DogPlayerInterface):
    def __init__(self) -> GUI:
        self._main_window: Tk = Tk()

        self._menubar: Menu = None

        self._hand_frame: Frame = None
        self._board_frame: Frame = None
        self._discard_frame: Frame = None
        self._info_frame: Frame = None

        self._hand_view: list[Label] = []
        self._board_view: list[Canvas] = []
        self._discard_view: list[Label] = []
        self._info_view: list[Label] = []
        self._current_info: str = "Bem-vindo!\nInicie uma\npartida\nusando o\nmenu"

        self._board: Board = Board()

        self.__build_main_window()
        self.__build_menubar()
        self.__build_hand_view()
        self.__build_discard_view()
        self.__build_info_view()

        player_name: str = simpledialog.askstring(title="Identificação do jogador", prompt="Qual seu nome?")
        self.dog_server_interface: DogActor = DogActor()
        message: str = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

        self._main_window.mainloop()

    def __build_menubar(self):
        self._menubar = Menu(self._main_window)
        self._menubar.option_add("tearOff", False)
        self._main_window["menu"] = self._menubar

        self.main_menu = Menu(self._menubar)
        self._menubar.add_cascade(menu=self.main_menu, label="Principal")

        self.main_menu.add_command(label="Iniciar jogo", command=self.start_match)
        self.main_menu.add_command(label="Fechar", command=self._main_window.destroy)

    def __build_main_window(self):
        self._main_window.title("Sequência")
        self._main_window.geometry("1600x900")
        self._main_window.resizable(False, False)
        self._main_window["bg"] = "darkblue"

        self._hand_frame = Frame(self._main_window, bg="black")
        self._hand_frame.grid(padx=100, pady=0, row=0, column=0, rowspan=2)

        self._board_frame = Frame(self._main_window, bg="black")
        self._board_frame.grid(padx=50,pady=6, row=0, column=1, rowspan=2)

        self._discard_frame = Frame(self._main_window, bg="black")
        self._discard_frame.grid(padx=100, pady=0, row=0, column=2)

        self._info_frame = Frame(self._main_window, bg="black")
        self._info_frame.grid(padx=100, pady=20, row=1, column=2)

    def __build_hand_view(self):
        for i in range(7):
            label = Label(self._hand_frame, bd=2)
            label.bind("<Button-1>", lambda event, index=i: self.hand_click(event, index))
            label.grid(row=i%4, column=i//4)
            self._hand_view.append(label)
        text_hand = Label(self._hand_frame, bg="white", text="Mão", font="monospace 30")
        text_hand.grid(row=3, column=1)

    def __build_board_view(self):
        self._board_view = []
        for index, board_place in enumerate(self._board.board_places):
            height = board_place.card.image.height()
            width = board_place.card.image.width()

            canvas = Canvas(self._board_frame, width=width, height=height)
            canvas.create_image(0, 0, anchor=NW, image=board_place.card.image, tags="image")
            canvas.bind("<Button-1>", lambda event, index=index: self.board_click(event, index))
            canvas.grid(row=index//10, column=index%10)

            self._board_view.append(canvas)

    def __build_discard_view(self):
        label = Label(self._discard_frame, bd=2)
        label.grid(row=0, column=0)
        self._discard_view.append(label)

        text_discard = Label(self._discard_frame, bg="white", text="Descarte", font="monospace 30")
        text_discard.grid(row=1, column=0)

    def __build_info_view(self):
        label = Label(self._info_frame, bg="gray", text=self._current_info, font="monospace 20")
        label.grid(row=1, column=0)
        self._info_view.append(label)

        text_info = Label(self._info_frame, bg="white", text="Info", font="monospace 30")
        text_info.grid(row=0,column=0)

    def __update_view(self):
        self.__update_board_view()
        self.__update_hand_view()
        self.__update_discard_view()
        self.__update_info_view()
        self._main_window.update()

    def __update_hand_view(self):
        images = [card.image for card in self._board.local_player.hand]
        for (label, image) in zip_longest(self._hand_view, images, fillvalue=""):
            label.configure(image=image)

    def __update_board_view(self):
        chip_radius = 20

        for index, board_place in enumerate(self._board.board_places):
            canvas = self._board_view[index]

            canvas.itemconfig("image", image=board_place.card.image)

            height = board_place.card.image.height()
            width = board_place.card.image.width()

            if board_place.player_in_place is not None:
                canvas.create_oval(width/2 - chip_radius,
                                  height/2 - chip_radius,
                                  width/2 + chip_radius,
                                  height/2 + chip_radius,
                                  fill=board_place.player_in_place.chips_color,
                                  tags="chip")
            elif canvas.gettags("chip"):
                self._board_view[index].delete("chip")

    def __update_discard_view(self):
        discard_pile_top = self._board.deck.discard_pile_top()
        if discard_pile_top is not None:
            self._discard_view[0].configure(image=discard_pile_top.image)

    def __update_info_view(self):
        self._info_view[0].configure(text=self._current_info)

    def hand_click(self, event, index):
        match_status = self._board.match_status

        if match_status == Status.YOUR_TURN_CARD:
            move_to_send = {}
            move_to_send, info = self._board.pick_card(index)

            self._current_info = info

            if move_to_send != {}:
                self.dog_server_interface.send_move(move_to_send)
        elif match_status == Status.OPPONENT_TURN:
            self._current_info = "Vez do\noponente"

        self.__update_view()

    def board_click(self, event, index):
        match_status = self._board.match_status

        if match_status == Status.YOUR_TURN_BOARD:
            move_to_send = {}
            info = ""
            move_to_send, info = self._board.select_board_place(index)

            self._current_info = info

            if move_to_send != {}:
                self.dog_server_interface.send_move(move_to_send)
        elif match_status == Status.OPPONENT_TURN:
            self._current_info = "Vez do\noponente"

        self.__update_view()

    def start_match(self):
        match_status = self._board.match_status

        if match_status == Status.STARTING:
            answer = messagebox.askyesno("INICIAR", "Deseja iniciar uma nova partida?")
            if answer:
                start_status = self.dog_server_interface.start_match(2)
                code = start_status.get_code()
                message = start_status.get_message()
                if code == "0" or code == "1":
                    messagebox.showinfo(message=message)
                else: # code == "2"
                    players = start_status.get_players()
                    player_id = start_status.get_local_id()
                    self._current_info = self._board.start_match(players, player_id)
                    messagebox.showinfo(message=start_status.get_message())

                    self.__build_board_view()
                    self.__update_view()

    def start_game(self):
        match_status = self._board.match_status
        if match_status == Status.FINISHED or match_status == Status.WITHDRAW:
            self._board.reset_game()
            self.__update_view()

    def receive_start(self, start_status):
        self.start_game()
        players = start_status.get_players()
        local_player_id = start_status.get_local_id()
        self._current_info = self._board.start_match(players, local_player_id)

        self.__build_board_view()
        self.__update_view()

    def receive_withdrawal_notification(self):
        self._board.receive_withdrawal_notification()
        self._current_info = "Desistência\ndo oponente"
        self.__update_view()

    def receive_move(self, move: dict):
        info = self._board.receive_move(move)
        self._current_info = info
        self.__update_view()
