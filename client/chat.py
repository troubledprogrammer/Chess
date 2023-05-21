"""
Handles the chat portion of the window
"""

import pygame as pg
from time import time as get_sys_time
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
    def __init__(self, window, name):
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
        self.cursor = pg.Surface((2, 0))
        self.cursor_pos = 0, 0

        # data
        self.messages = [
            Line(f"{name} (3271) vs GMHikaru (2909)"),
            Line("NEW GAME", True),
        ]
        self.name = name
        self.typed = ""
        self.focused = False
        self._update_surface()

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if event.button == 1:
                    if self.pos[0] <= mouse_x <= WINDOW_SIZE_X and\
                            self.pos[1] <= mouse_y <= WINDOW_SIZE_Y:
                        self.focused = True
                        print("focused")
                    else:
                        self.focused = False
                        print("unfocused")
            if self.focused:
                if event.type == pg.KEYDOWN and event.key not in [pg.K_TAB]:
                    if event.key == pg.K_BACKSPACE:
                        self.typed = self.typed[:-1]
                    elif event.key == pg.K_RETURN:
                        self.send_message()
                    else:
                        self.typed = self.typed + event.unicode
                    self._update_surface()

    def draw(self):
        self.display.blit(self.surface, self.pos)
        if self.focused and get_sys_time() % 1 > 0.5:
            self.display.blit(self.cursor, (self.cursor_pos[0]+self.pos[0], self.cursor_pos[1] + self.pos[1]))

    def send_message(self):
        # TODO send self.typed
        self.add_chat(self.typed)
        self.typed = ""

    def add_chat(self, text):
        self.messages.insert(0, Line(text))
        self._update_surface()

    def add_info(self, data):
        # TODO add info
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

        # cursor
        if self.cursor.get_height() != rect.height:
            self.cursor = pg.Surface((2, rect.height))
            self.cursor.fill(CHAT_COLOUR)
        if self.typed == "": self.cursor_pos = rect.topleft
        else: self.cursor_pos = rect.topright

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
    class X:
        display = None
    test = Chat(X(), "MilesWij")
