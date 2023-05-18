"""
Handles the display and io
"""
import pygame as pg
from constants import *


class Window:
    def __init__(self):
        # display
        pg.init()
        self.display = pg.display.set_mode((800, 800))
        pg.display.set_caption("chess")

        # textures
        self.board_image = pg.image.load(".../assets/board/wood/board.png")
        self.board_image = pg.transform.smoothscale(self.board_image, (800, 800))
        self.piece_images = {}
        for c in "pnbrqk":
            w = pg.image.load(f".../assets/pieces/default/w{c}.png")
            w = pg.transform.smoothscale(w, (100, 100))
            b = pg.image.load(f".../assets/pieces/default/b{c}.png")
            b = pg.transform.smoothscale(b, (100, 100))
            self.piece_images[c] = {WHITE_PIECE: w, BLACK_PIECE: b}
        icon = pg.image.load(".../assets/window/icon.png").convert_alpha()
        pg.display.set_icon(icon)
