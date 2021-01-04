"""Module containg Tetromino class

Tetromino class is used in main file - game.py

It is responsible for:
    - drawing buffer (currently falling tetromino)
    - detecting collision with gameboard (with borders and previously fallen blocks)
    - moving buffer (left/right/rotate/fall)
"""

import random

import pygame

import config

class Tetromino:
    """Implemented Tetromino:
        4 x 4 array which holds actuall shape of Tetromino
        x, y cooridantes of top left element of this array on gameboard
    """

    def __init__(self, type, times_rotated=0, x=4, y=0):
        """Initializes falling tetromino."""

        # cooridantes of [0][0] (top left element) of buffor on gameboard
        self.current_x = x
        self.current_y = y

        # self.buffer is 4x4 array which holds current shape and rotation of tetromino

        if type in config.TETROMINO_SHAPES:
            self.buffer = config.TETROMINO_SHAPES[type]
            for _ in range(times_rotated):
                self.rotate()

    @staticmethod
    def get_random_tetromino():
        return Tetromino(
            type=random.choice(list(config.TETROMINO_SHAPES)),
            times_rotated=random.randint(0, 3),
            x=4, y=0
        )

    def rotate(self, clockwise=True) -> None:
        """Roates bufor clockwise or counterclockwise"""

        rotated_array = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        for i in range(0, 4):
            for j in range(0, 4):
                rotated_array[i][j] = self.buffer[3-j][i] if clockwise else self.buffer[j][3-i]
        self.buffer = rotated_array

    def change_position(self, pressed_key: int) -> None:
        """Changes position and/or buffer coressponding to pressed key
        pygame.K_XXX is an int
        """
        if pressed_key == pygame.K_UP:
            self.rotate()
        elif pressed_key == pygame.K_LEFT:
            self.current_x -= 1
        elif pressed_key == pygame.K_RIGHT:
            self.current_x += 1
        elif pressed_key == pygame.K_DOWN:
            self.current_y += 1

    def undo_move(self, pressed_key: int) -> None:
        """Changes position and/or buffer to previous value(s) coressponding to pressed key"""

        if pressed_key == pygame.K_UP:
            self.rotate(clockwise=False)
        elif pressed_key == pygame.K_LEFT:
            self.current_x += 1
        elif pressed_key == pygame.K_RIGHT:
            self.current_x -= 1
        elif pressed_key == pygame.K_DOWN:
            self.current_y -= 1

    def calculate_buffer_drawing_coordinates(self) -> tuple:
        """Calculates drawing coordinates necessarry while drawing single block"""
        rect_bufor_x = (self.current_x * config.BLOCK_SIZE) + config.GAME_BOARD_COORDS.left
        rect_bufor_y = (self.current_y * config.BLOCK_SIZE) + config.GAME_BOARD_COORDS.top

        return rect_bufor_x, rect_bufor_y

    def draw(self, screen) -> None:
        """Draws 4 x 4 bufor of currently falling tetromino"""

        rect_bufor_x, rect_bufor_y = self.calculate_buffer_drawing_coordinates()

        for i, row in enumerate(self.buffer):
            for j, elem in enumerate(row):
                if elem == config.BUFFER_BLOCK:
                    pygame.draw.rect(
                        screen,
                        config.Color.LIGHTBLUE.value,
                        (rect_bufor_x+(j*config.BLOCK_SIZE),
                         rect_bufor_y+(i*config.BLOCK_SIZE),
                         config.BLOCK_SIZE,
                         config.BLOCK_SIZE)
                    )
