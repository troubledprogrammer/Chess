"""
Stores the class for the info bar containing the player info and game clock
"""

import pygame as pg
from constants import *


class Clock:
    def __init__(self, parent, time, colour):
        self.time = time
        self.parent = parent
        self.display = self.parent.surface

        self.img = pg.image.load(f"assets/clock/{colour}.png")
        self.rect = self.img.get_rect(bottomright=(INFO_BAR_SIZE_X-CHAT_PADDING, INFO_BAR_SIZE_Y-CHAT_PADDING))

    def draw(self):
        self.display.blit(self.img, self.rect)
        # draw 