"""Module with Gameboard class

Gameboard class is used in main file - game.py

It is responsible for:
    - drawing board
    - holding falling tetromino (buffer)
    - holding information about blocks that had fallen earlier
    - detecting which rows should be deleted (and then moving all above one block down)
"""

import pygame

import config
import tetromino


class Gameboard:
    """Implementing board:
        - where Tetromino falls and moves
        - where fallen Tetromino joins to board
    """

    def __init__(self):
        self.initialize_board()

    def initialize_board(self):
        """Create and set inital values of self.fields

        Types of blocks used at beginning of the game:
        - config.EMPTY_BLOCK for all blocks where Tetromino can move
        - config.BORDER_BLOCK for borderline left and right column blocks and all bottom blocks (undeletable)
        """

        # self.fields are array where Tetromino falls
        self.fields = [[config.EMPTY_BLOCK for i in range(0, config.BOARD_COLUMNS)] for j in range(0, config.BOARD_ROWS)]

        for i in range(0, config.BOARD_BOTTOM_ROW): # except the last row (bottom line)
            self.fields[i][config.BOARD_LEFT_BORDER]  = config.BORDER_BLOCK
            self.fields[i][config.BOARD_RIGHT_BORDER] = config.BORDER_BLOCK

        for i in range(0, config.BOARD_COLUMNS):
            self.fields[config.BOARD_BOTTOM_ROW][i] = config.BORDER_BLOCK

    def draw_single_block(self, screen, color, x_rect, y_rect):
        """Function responsible for drawing single block of gameboard"""
        pygame.draw.rect(
            screen,
            color,
             (config.GAME_BOARD_COORDS.left + x_rect * config.BLOCK_SIZE,
              config.GAME_BOARD_COORDS.top  + y_rect * config.BLOCK_SIZE,
              config.BLOCK_SIZE, config.BLOCK_SIZE)
        )

    def draw_gameboard_blocks(self, screen):
        """Drawing gameboard fields (borders, empty and fallen blocks)"""

        for i, row in enumerate(self.fields):
            for j, board_elem in enumerate(row):
                self.draw_single_block(screen, config.COLORS_FOR_BLOCK[board_elem], j, i)

    def attach_tetromino_blocks(self, tetromino):
        """Attaching buffered blocks of Tetromino that has just fallen"""

        y, x = tetromino.current_y, tetromino.current_x

        for i, row in enumerate(tetromino.buffer):
            for j, elem in enumerate(row):
                if tetromino.buffer[i][j] == config.BUFFER_BLOCK:
                    self.fields[y + i][x + j] = config.FALLEN_BLOCK

    def is_row_fully_filled(self, row):
        return (config.EMPTY_BLOCK not in row[config.BOARD_FIRST_COLUMN:config.BOARD_LAST_COLUMN+1])

    def delete_rows(self):
        """Check if specified row is empty; if yes deletes it and moves all blocks down"""

        rows_to_detele   = [] # indexes of filled rows
        blocks_to_change = range(config.BOARD_FIRST_COLUMN, config.BOARD_LAST_COLUMN+1)

        for i, row in enumerate(self.fields[:-1]): # except the bottom line of Gameboard
            if self.is_row_fully_filled(row):
                rows_to_detele.append(i)

        for row_index in rows_to_detele:
            for block in blocks_to_change:
                self.fields[row_index][block] = config.EMPTY_BLOCK # delete row

            for i in range(row_index-1, 0, -1): # from bottom to up
                for j in blocks_to_change:
                    self.fields[i+1][j] = self.fields[i][j] # moves all blocks within row one row lower
