#!/bin/python3.8
"""Global variables used to configure neccessary stuff within project

This module contains constans for:
    - window size
    - coordinates and sizes of every objects of the screen
    - colors
    - Tetromino shapes
    - time constans

"""
import collections
import enum

# Window size (in pixels)
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

# Size of Gameboard (fields array) - numbers of columns and rows
# The oryginal version of Tetris (from 1989 on Nintend Entertaiment System) has Gameboard with size:
# 22 rows and 10 columns within Tetromino can fall/move
# There are two additional columns (for left and right border) and one additional row (for bottom line)
BOARD_COLUMNS = 10 + 2 # +2 stands for left and right border columns
BOARD_ROWS    = 22 + 1 # +1 stand for bottom border row

# Playable blocks const. used to avoid magic numbers and expressions
BOARD_FIRST_COLUMN = 1
BOARD_LAST_COLUMN  = BOARD_COLUMNS-2
BOARD_FIRST_ROW    = 0
BOARD_LAST_ROW     = BOARD_ROWS-2

# Border const. used to avoid magic numbers and expressions
BOARD_LEFT_BORDER  = 0
BOARD_RIGHT_BORDER = BOARD_COLUMNS-1
BOARD_BOTTOM_ROW   = BOARD_ROWS-1

BORDER_BLOCK = -1
BUFFER_BLOCK = 1
EMPTY_BLOCK  = 0
FALLEN_BLOCK = 2

# Colors used within game to draw
class Color(enum.Enum):
    """Make human-readable aliases of colors used in game"""
    BLACK     = (0, 0, 0)
    DARKRED   = (100, 10, 10)
    LIGHTBLUE = (173, 216, 230)
    ORANGE    = (255, 165, 0)
    RED       = (220, 20, 60)


# Dict. for easier color use within classes
COLORS_FOR_BLOCK = {
    BORDER_BLOCK : Color.BLACK.value,
    # BUFFER_BLOCK : Co
    EMPTY_BLOCK : Color.RED.value,
    FALLEN_BLOCK : Color.ORANGE.value,
}





# Sizes within game:
BLOCK_SIZE   = 15 # (in pixels) single block of tetromino/gameboard
BOARD_WIDTH  = BLOCK_SIZE * (BOARD_COLUMNS+2)
BOARD_HEIGHT = BLOCK_SIZE * (BOARD_ROWS)

Gameboard_coords_on_screen = collections.namedtuple('Gameboard_coords_on_screen', ['top', 'left'])
# For drawing gameboard with borders around
BOARD_WITH_BORDER_COORDS = Gameboard_coords_on_screen(
    top  = (SCREEN_HEIGHT / 2 - BOARD_HEIGHT / 2),
    left = (SCREEN_WIDTH / 2 - BOARD_WIDTH / 2),
)
# For actuall gameboard - when tetromino falls etc.
GAME_BOARD_COORDS = Gameboard_coords_on_screen(
    top  = BOARD_WITH_BORDER_COORDS.top,
    left = BOARD_WITH_BORDER_COORDS.left + BLOCK_SIZE,
)

GAME_SINGLE_FRAME_SEC = 0.0001 # interval between single steps
TIME_STEPS_TO_FALL_BUFFER = 200 # how many steps is needed to fall tetromino one block down

TETROMINO_SHAPES = {
    "I" : [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
    ],
    "Z" : [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0],
    ],
    "S" : [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
    ],
    "J" : [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
    ],
    "L" : [
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
    ],
    "T" : [
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
    ],
    "O" : [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
}
