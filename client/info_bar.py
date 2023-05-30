"""
Stores the class for the info bar containing the player info and game clock
"""

import pygame as pg
import _thread as threading
from time import sleep, time
from constants import *


class Clock:
    def __init__(self, parent, time, colour):
        self.time = time
        self.parent = parent
        self.display = self.parent.surface

        self.img = pg.image.load(f"assets/clock/{colour}.png")
        self.rect = self.img.get_rect(bottomright=(INFO_BAR_SIZE_X-CLOCK_PADDING, INFO_BAR_SIZE_Y//2))

    def draw(self):
        self.display.blit(self.img, self.rect)
        # DRAW TEXT


class InfoBar:
    def __init__(self, parent, colour):
        self.parent = parent
        self.display = self.parent.display
        self.surface = pg.Surface((INFO_BAR_SIZE_X, INFO_BAR_SIZE_Y))
        self.colour = colour

        self.clock = Clock(self, 10, )