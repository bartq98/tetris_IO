#!/bin/env python

"""Module contains User Interface class

"""
import time

import pygame

import config
import game
import gameboard
import tetromino

class UserInterface():

    def initialize_window(self):
        """Creates window"""
        pygame.init()
        pygame.display.set_caption("Tetris by Bartłomiej Bieńko")

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.screen.fill(config.Color.DARKRED.value)

    def clear_window(self, screen : pygame.Surface) -> None:
        """Clear window - set whole screen as background color"""
        screen.fill(config.COLORS_FOR_MENU["BACKGROUND"])

    def __init__(self):
        """Creates window"""
        self.initialize_window()

    def draw_menu(self) -> None:
        pass


if __name__ == "__main__":
    ui = UserInterface()
    pygame.display.update()
    time.sleep(4)