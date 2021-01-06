from abc import abstractmethod

import pygame

import config

class Drawable():

    def draw_single_block(self, screen, color, x_rect, y_rect) -> None:
        """Function responsible for drawing single block of gameboard"""
        pygame.draw.rect(
            screen,
            color,
             (config.BOARD_WITH_BORDER_COORDS.left + x_rect * config.BLOCK_SIZE,
              config.BOARD_WITH_BORDER_COORDS.top  + y_rect * config.BLOCK_SIZE,
              config.BLOCK_SIZE, config.BLOCK_SIZE)
        )

    @abstractmethod
    def draw(self) -> None:
        pass