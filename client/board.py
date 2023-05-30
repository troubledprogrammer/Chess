"""
File containing the board section of the window
"""
import pygame as pg
from constants import *


def fen_to_pos(fen):
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
    """
    Class for board part of the clinet UI
    """
    def __init__(self, window, position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        # parent window
        self.window = window
        self.display = self.window.display

        # textures - board
        piece_size = BOARD_SIZE // 8
        self.board_image = pg.image.load(f"assets/board/{BOARD_STYLE}/board.png")
        self.board_image = pg.transform.smoothscale(self.board_image, (BOARD_SIZE, BOARD_SIZE))

        # textures - pieces
        self.piece_images = {}
        for c in "pnbrqk":
            w = pg.image.load(f"assets/pieces/{PIECE_STYLE}/w{c}.png")
            w = pg.transform.smoothscale(w, (piece_size, piece_size))
            b = pg.image.load(f"assets/pieces/{PIECE_STYLE}/b{c}.png")
            b = pg.transform.smoothscale(b, (piece_size, piece_size))
            self.piece_images[c.upper()] = w
            self.piece_images[c] = b

        # textures - valid move
        rgba = VALID_MOVE_RGBA
        pos = BOARD_SIZE // 16, BOARD_SIZE // 16
        self.valid_move_image = pg.Surface((BOARD_SIZE//8, BOARD_SIZE//8), pg.SRCALPHA)
        pg.draw.circle(self.valid_move_image, rgba, pos, BOARD_SIZE//48, 0)
        self.valid_capture_image = pg.Surface((BOARD_SIZE//8, BOARD_SIZE//8), pg.SRCALPHA)
        pg.draw.circle(self.valid_move_image, rgba, pos, BOARD_SIZE//24, BOARD_SIZE//64)

        # position data
        self.position = fen_to_pos(position)

    def update(self, events):
        pass

    def draw(self):
        # board
        self.display.blit(self.board_image, (0, INFO_BAR_SIZE_Y))

        # pieces
        self._draw_pieces()

        # decorations
        self._draw_decorations()

        # valid moves
        self._draw_valid_moves()

    def _draw_pieces(self):
        square_size = BOARD_SIZE//8
        for index, piece in enumerate(self.position):
            if piece is not None:
                y, x = divmod(index, 8)
                xpos, ypos = x*square_size, y*square_size + INFO_BAR_SIZE_Y
                self.display.blit(self.piece_images[piece], (xpos, ypos))

    def _draw_decorations(self):
        pass

    def _draw_valid_moves(self):
        pass


if __name__ == "__main__":
    pass
