"""
File containing the board section of the window
"""
import pygame as pg
from constants import *

import chess.game as _chess
from chess.constants import *
from chess.conversions import coordinate_to_index


def fen_to_pos(fen):
    rows = fen.split(" ")[0].split("/")
    res = []
    for row in rows:
        for c in row:
            if not c.isnumeric():
                res.append(c)
            else:
                res.extend([None] * int(c))
    return res


def mouse_pos_to_index():
    x, y = pg.mouse.get_pos()
    x, y = x * 8 // BOARD_SIZE, (y - INFO_BAR_SIZE_Y) * 8 // BOARD_SIZE
    if not (0 <= x <= 7 and 0 <= y <= 7): return None
    return coordinate_to_index((x, y))


class Board:
    """
    Class for board part of the clinet UI
    """
    SQUARE_SIZE = BOARD_SIZE // 8

    def __init__(self, window):
        # parent window
        self.game = window
        self.display = self.game.display

        # textures - board
        self.board_image = pg.image.load(f"assets/board/{BOARD_STYLE}/board.png")
        self.board_image = pg.transform.smoothscale(self.board_image, (BOARD_SIZE, BOARD_SIZE))

        # textures - pieces
        self.piece_images = {}
        for c in "pnbrqk":
            w = pg.image.load(f"assets/pieces/{PIECE_STYLE}/w{c}.png")
            w = pg.transform.smoothscale(w, (self.SQUARE_SIZE, self.SQUARE_SIZE))
            b = pg.image.load(f"assets/pieces/{PIECE_STYLE}/b{c}.png")
            b = pg.transform.smoothscale(b, (self.SQUARE_SIZE, self.SQUARE_SIZE))
            p = {WHITE: w, BLACK: b}
            self.piece_images[c] = p

        # textures - valid move
        rgba = VALID_MOVE_RGBA
        pos = self.SQUARE_SIZE // 2, self.SQUARE_SIZE // 2
        self.valid_move_image = pg.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.valid_move_image, rgba, pos, self.SQUARE_SIZE // 6, 0)
        self.valid_capture_image = pg.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pg.SRCALPHA)
        pg.draw.circle(self.valid_capture_image, rgba, pos, self.SQUARE_SIZE // 3, self.SQUARE_SIZE // 8)

        self.valid_move_sprites = []

        # textures - highlighted squares
        rgba = HIGHLIGHTED_SQUARE_RGBA
        self.highlighted_square_image = pg.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pg.SRCALPHA)
        self.highlighted_square_image.fill(rgba)

        self.highlighted_square_indexes = set()

        # position data
        self.position = self.game.position

        # held piece sprite
        self.held_piece_img = None
        self.held_piece_index = None

        # click info
        self.right_click_pos = None

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    self._on_left_mouse_down()
                elif event.button == pg.BUTTON_RIGHT:
                    self._on_right_mouse_down()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT:
                    self._on_left_mouse_up()
                elif event.button == pg.BUTTON_RIGHT:
                    self._on_right_mouse_up()

    def _on_left_mouse_down(self):
        self.highlighted_square_indexes.clear()

        i = mouse_pos_to_index()
        if i is None: return
        s = self.position.position[i]
        if s.has_piece():
            self.held_piece_index = i
            self.held_piece_img = self.piece_images[s.piece.type][s.piece.colour]

            for move in self.position.get_legal_moves():
                if move.current_pos == self.held_piece_index:
                    # draw possible move
                    y, x = divmod(move.target_pos, 8)
                    pos = x * self.SQUARE_SIZE, y * self.SQUARE_SIZE + INFO_BAR_SIZE_Y
                    img = self.valid_capture_image if self.position.position[move.target_pos].has_piece() else self.valid_move_image
                    self.valid_move_sprites.append((img, pos))

    def _on_right_mouse_down(self):
        i = mouse_pos_to_index()
        if i is not None:
            self.right_click_pos = i

    def _on_left_mouse_up(self):
        i = mouse_pos_to_index()
        if self.held_piece_index is not None and i is not None:
            m = _chess.Move(self.held_piece_index, i)
            self.game.make_move(m)
        self.held_piece_index = None
        self.held_piece_img = None
        self.valid_move_sprites = []

    def _on_right_mouse_up(self):
        i = mouse_pos_to_index()
        if i is not None:
            if i == self.right_click_pos:
                if i not in self.highlighted_square_indexes:
                    self.highlighted_square_indexes.add(i)
                else:
                    self.highlighted_square_indexes.remove(i)
            else:
                # TODO draw arrow
                pass
        self.right_click_pos = None

    def draw(self):
        self.display.blit(self.board_image, (0, INFO_BAR_SIZE_Y))
        self._draw_decorations()
        self._draw_pieces()
        self._draw_valid_moves()
        self._draw_held()

    def _draw_pieces(self):
        for index, square in enumerate(self.position.position):
            if square.has_piece() and index != self.held_piece_index:
                y, x = divmod(index, 8)
                xpos, ypos = x * self.SQUARE_SIZE, y * self.SQUARE_SIZE + INFO_BAR_SIZE_Y
                self.display.blit(self.piece_images[square.piece.type][square.piece.colour], (xpos, ypos))

    def _draw_held(self):
        if self.held_piece_index is not None:
            x, y = pg.mouse.get_pos()
            x, y = max(0, min(x, BOARD_SIZE)), max(INFO_BAR_SIZE_Y, min(y-INFO_BAR_SIZE_Y, BOARD_SIZE)+INFO_BAR_SIZE_Y)
            r = self.held_piece_img.get_rect(center=(x,y))
            self.display.blit(self.held_piece_img, r)

    def _draw_decorations(self):
        for i in self.highlighted_square_indexes:
            y, x = divmod(i, 8)
            xpos, ypos = x * self.SQUARE_SIZE, y * self.SQUARE_SIZE + INFO_BAR_SIZE_Y
            self.display.blit(self.highlighted_square_image, (xpos, ypos))

    def _draw_valid_moves(self):
        for sprite in self.valid_move_sprites:
            self.display.blit(*sprite)


if __name__ == "__main__":
    pass
