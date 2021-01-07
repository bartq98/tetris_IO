#!/bin/env python
"Simple Tetris-inspired game written with Python and PyGame"

import random
import time
import timeit

import pygame

import config
import gameboard
import tetromino


class Game():

    def __init__(self, screen : pygame.Surface, level : int):

        self.gameboard = gameboard.Gameboard()
        self.level     = level
        self.score     = 0
        self.screen    = screen

    def add_score(self, deleted_rows_count: int) -> None:
        if deleted_rows_count == 0:
            self.score += 0
        elif 1 <= deleted_rows_count <= 3:
            self.score += 100 * deleted_rows_count * self.level
        elif deleted_rows_count == 4:
            self.score += 200 * deleted_rows_count * self.level

    def is_time_to_fall(self, time_units_done : int) -> bool:
        return time_units_done == config.LEVEL_STEPS[self.level]

    def after_tetromino_fall(self) -> None:
        self.gameboard.attach_tetromino_blocks()
        self.gameboard.generate_new_tetromino()

    def is_gameover(self) -> bool:
        """Called only after new Tetromino is created"""
        return self.gameboard.is_tetromino_colliding()

    def main_gameloop(self) -> None:
        """Where game happens"""

        time_units_done = 0

        while True:

            self.gameboard.draw(self.screen)
            time.sleep(config.GAME_SINGLE_FRAME_SEC) # sleeps for every 50 miliseconds # TODO zmienić jakiejś funkcji
            self.gameboard.move_tetromino()

            time_units_done += 1

            if self.is_time_to_fall(time_units_done):

                time_units_done = 0
                has_falled = self.gameboard.fall_tetromino_down()
                
                if has_falled:
                    self.after_tetromino_fall()

                    if self.is_gameover():
                        break
                
                rows = self.gameboard.delete_rows()
                self.add_score(rows)

            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    screen.fill(config.Color.DARKRED.value)
    gejm = Game(screen, 2)
    gejm.main_gameloop()
