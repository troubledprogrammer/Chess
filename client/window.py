"""
Handles the display and io
"""
import sys
import pygame as pg
from constants import *
from board import Board


class Window:
    def __init__(self):
        # display
        pg.init()
        self.display = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pg.display.set_caption("chess")

        # textures
        icon = pg.image.load("assets/icon.png").convert_alpha()
        pg.display.set_icon(icon)

        # board
        self.board = Board(self.display)

    def update(self):
        self.display.fill((0, 0, 0))
        self.board.draw()
        pg.display.update()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()

            self.update()

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    win = Window()
    win.run()
