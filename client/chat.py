"""
Handles the chat portion of the window
"""

import pygame as pg
from constants import *
from dataclasses import dataclass

@dataclass
class Line:
    text: str
    bold: bool = False
    italic: bool = False


class Chat:
    """
    Chat class
    """
    def __init__(self, window):
        # parent window
        self.window = window
        self.display = self.window.display
        self.surface = pg.Surface((CHAT_SIZE_X, CHAT_SIZE_Y))
        self.surface.fill(CHAT_BG_COLOUR)
        self.pos = (BOARD_SIZE, MOVE_HISTORY_SIZE_Y)

        # textures
        pg.font.init()
        font_folder = f"assets/fonts/{CHAT_FONT}/{{}}.ttf"
        self.font_normal = pg.font.Font(font_folder.format("regular"), CHAT_FONT_SIZE)
        self.font_bold = pg.font.Font(font_folder.format("bold"), CHAT_FONT_SIZE)
        self.font_italic = pg.font.Font(font_folder.format("italic"), CHAT_FONT_SIZE)

        # data
        self.messages = [
            Line("Miles (3271) vs Hikaru (2909)"),
            Line("NEW GAME", True),
        ]
        self.typed = ""
        self._update_surface()

    def update(self, events):
        pass

    def draw(self):
        self.display.blit(self.surface, self.pos)

    def add_chat(self, text):
        self.messages.insert(0, Line(text))
        self._update_surface()

    def add_info(self, data):
        # add info
        self._update_surface()

    def _update_surface(self):
        # clear
        self.surface.fill(CHAT_BG_COLOUR)

        # text input
        y = self.surface.get_height() - CHAT_PADDING
        img = self.font_normal.render(self.typed if self.typed != "" else CHAT_INPUT_TEXT, True, CHAT_COLOUR)
        rect = img.get_rect(bottomleft=(CHAT_PADDING, y))
        y -= img.get_height()
        self.surface.blit(img, rect)
        pg.draw.line(self.surface, CHAT_COLOUR, (0, y), (self.surface.get_width(), y))

        # sent messages
        for message in self.messages:
            if message.bold:
                img = self.font_bold.render(message.text, True, CHAT_COLOUR)
            else:
                img = self.font_normal.render(message.text, True, CHAT_COLOUR)
            rect = img.get_rect(bottomleft=(CHAT_PADDING, y))
            y -= img.get_height()
            self.surface.blit(img, rect)

if __name__ == "__main__":
    class x:
        display = None
    test = Chat(x())