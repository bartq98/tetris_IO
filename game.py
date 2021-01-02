#!/bin/env python
"Simple Tetris-inspired game written with Python and PyGame"
import random
import time

import pygame

import config
import gameboard
import tetromino


def pre_configure_window():
    """Configure whole stuff around game"""
    
    pygame.display.set_caption("Tetris by Bartq98")
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    screen.fill(config.Color.DARKRED.value)
    return screen

def game():
    """Runs whole game"""
    pygame.init()
    screen = pre_configure_window()

    actuall_gameboard = gameboard.Gameboard()

    time_steps_done_before_fall = 0
    game_over = False

    # main gameloop
    while not game_over:

        actuall_gameboard.draw_gameboard_blocks(screen) # only gameboard are redrawing in all frame
        time.sleep(config.GAME_SINGLE_FRAME_SEC) # sleeps for every 50 miliseconds

        # buffer.move(actuall_gameboard) # controlled from keyboard
        actuall_gameboard.move_tetromino()

        time_steps_done_before_fall += 1
        if time_steps_done_before_fall == config.TIME_STEPS_TO_FALL_BUFFER:
            has_falled = actuall_gameboard.fall_tetromino_down()
            
            if has_falled:
                actuall_gameboard.attach_tetromino_blocks()
                actuall_gameboard.falling_tetromino = tetromino.Tetromino("L")
                print(actuall_gameboard.falling_tetromino)
                print(f"Current pos: ", actuall_gameboard.falling_tetromino.current_y)
                if actuall_gameboard.is_tetromino_colliding(): # as soon as has been made
                    game_over = True
                    print(f"Thank You for your play - waiting to see u next time!")
                actuall_gameboard.delete_rows()

            time_steps_done_before_fall = 0

        pygame.display.update()


class Game():

    def __init__(self):

        # self.screen()

        self.gameboard = gameboard.Gameboard()
        self.buffer = tetromino.Tetromino.get_random_tetromino()

        time_units_before_fall = 0
        gameover = 0


    def __run__(self):
        pass
        # initialize_game
        # gameloop


# Where magic happens...
if __name__ == "__main__":
    game()
