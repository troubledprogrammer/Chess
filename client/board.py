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
        # board
        self.display.blit(self.board_image, (0, 0))

        # pieces
        self._draw_pieces()

        # decorations
        self._draw_decorations()

    def _draw_pieces(self):
        square_size = WINDOW_SIZE//8
        for index, piece in enumerate(self.position):
            if piece is not None:
                y, x = divmod(index, 8)
                xpos, ypos = x*square_size, y*square_size
                self.display.blit(self.piece_images[piece], (xpos, ypos))

    def _draw_decorations(self):
        pass


if __name__ == "__main__":
    pass
