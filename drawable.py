from abc import abstractmethod

import pygame

import config

class Drawable():

    def draw_single_block(self, screen : pygame.Surface, block_type : int, x_rect : int, y_rect : int) -> None:
        """Function responsible for drawing single block of gameboard"""
        pygame.draw.rect(
            screen,
            config.COLORS_FOR_BLOCK[block_type],
             (config.BOARD_WITH_BORDER_COORDS.left + x_rect * config.BLOCK_SIZE,
              config.BOARD_WITH_BORDER_COORDS.top  + y_rect * config.BLOCK_SIZE,
              config.BLOCK_SIZE, config.BLOCK_SIZE)
        )

    @abstractmethod
    def draw(self) -> None:
        pass