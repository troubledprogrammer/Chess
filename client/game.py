"""
Handles the display and io
"""
import sys
import pygame as pg
from constants import *
from board import Board
from chat import Chat

import chess.chess as _chess


class Game:
    """
    Class for the client UI
    """
    def __init__(self):
        # display
        pg.init()
        self.display = pg.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
        pg.display.set_caption("Chess")

        # textures
        icon = pg.image.load("assets/icon.png")
        pg.display.set_icon(icon)

        # board
        self.position = _chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.board = Board(self)

        # chat
        self.name = "MilesWij"
        self.chat = Chat(self, self.name)

        # time
        self.time = pg.time.Clock()

    def make_move(self, move):
        """
        Sends a move to server and temporarily updates pos
        :param move: Move
        :return: None
        """
        # TODO IMPLEMENT
        print(move)
        if move.is_valid(self.position):
            self.position.make_move(move)

    def update(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

        self.board.update(events)
        self.chat.update(events)

        #print(1000/self.time.tick())

    def draw(self):
        self.display.fill((0, 0, 0))
        self.board.draw()
        self.chat.draw()

        pg.display.update()

    def run(self):
        while True:
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    win = Game()
    win.run()
