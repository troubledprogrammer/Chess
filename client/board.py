"""
File containing the board section of the window
"""
import pygame as pg
from constants import *

def fenToPos(fen):
    rows = fen.split(" ")[0].split("/")
    res = []
    for row in rows:
        for c in row:
            if not c.isnumeric():
                res.append(c)
            else:
                res.extend([None]*int(c))
    return res

class Board:
    def __init__(self, display, position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        # parent window
        self.display = display

        # textures
        self.board_image = pg.image.load("assets/board/wood/board.png")
        self.board_image = pg.transform.smoothscale(self.board_image, (800, 800))
        self.piece_images = {}
        for c in "pnbrqk":
            w = pg.image.load(f"assets/pieces/default/w{c}.png")
            w = pg.transform.smoothscale(w, (100, 100))
            b = pg.image.load(f"assets/pieces/default/b{c}.png")
            b = pg.transform.smoothscale(b, (100, 100))
            self.piece_images[c.upper()] = w
            self.piece_images[c] = b

        # position data
        self.position = fenToPos(position)

    def draw(self):
        self.display.blit(self.board_image, (0, 0))




if __name__ == "__main__":
    pass