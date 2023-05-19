"""
Handles the display and io
"""
import sys
import pygame as pg
from constants import *


class Window:
    def __init__(self):
        # display
        pg.init()
        self.display = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pg.display.set_caption("chess")

        # textures
        self.board_image = pg.image.load("assets/board/wood/board.png")
        self.board_image = pg.transform.smoothscale(self.board_image, (800, 800))
        self.piece_images = {}
        for c in "pnbrqk":
            w = pg.image.load(f"assets/pieces/default/w{c}.png")
            w = pg.transform.smoothscale(w, (100, 100))
            b = pg.image.load(f"assets/pieces/default/b{c}.png")
            b = pg.transform.smoothscale(b, (100, 100))
            self.piece_images[c] = {WHITE_PIECE: w, BLACK_PIECE: b}
        icon = pg.image.load("assets/icon.png").convert_alpha()
        pg.display.set_icon(icon)

    def update(self):
        self.display.fill((0, 0, 0))
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
