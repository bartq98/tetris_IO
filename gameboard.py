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

    # self.fields are array where Tetromino falls

    def __init__(self):
        self.initialize_board()

    def initialize_board(self):
        """
        Set inital values of self.fields:
            - config.EMPTY_BLOCK for all blocks where Tetromino can move
            - config.BORDER_BLOCK for borderline left and right column blocks and all bottom blocks (undeletable)
        """

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

    def draw_gameboard(self, screen):
        """Drawing gameboard within screen"""

        # used colors can be simply changed
        color_block  = config.Color.ORANGE.value
        color_border = config.Color.BLACK.value
        color_empty  = config.Color.RED.value

        for i, row in enumerate(self.fields):
            for j, board_elem in enumerate(row):
                if board_elem == config.EMPTY_BLOCK:
                    self.draw_single_block(screen, color_empty, j, i)
                elif board_elem == config.BORDER_BLOCK:
                    self.draw_single_block(screen, color_border, j, i)
                elif board_elem == config.FALLEN_BLOCK:
                    self.draw_single_block(screen, color_block, j, i)

    def add_blocks(self, tetromino):
        """Adding single blocks of fallen tetromino to self.fields => setting them o config.FALLEN_BLOCK"""
        y, x = tetromino.current_y, tetromino.current_x

        for i, row in enumerate(tetromino.buffer):
            for j, elem in enumerate(row):
                if tetromino.buffer[i][j] == config.BUFFER_BLOCK:
                    self.fields[y + i][x + j] = config.FALLEN_BLOCK

    def delete_lines(self):
        """Check if specified row is empty; if yes deletes it and moves all blocks down"""

        rows_to_detele   = [] # holds indexes of filled rows
        blocks_to_check  = slice(config.BOARD_FIRST_COLUMN, config.BOARD_LAST_COLUMN+1)
        blocks_to_change = range(config.BOARD_FIRST_COLUMN, config.BOARD_LAST_COLUMN+1)

        for i, row in enumerate(self.fields[:-1]): # except the bottom line of Gameboard
            if config.EMPTY_BLOCK in row[blocks_to_check]:
                continue
            else:
                rows_to_detele.append(i)

        for row_index in rows_to_detele:
            for block in blocks_to_change:
                self.fields[row_index][block] = config.EMPTY_BLOCK # delete row

            for i in range(row_index-1, 0, -1): # from bottom to up
                for j in blocks_to_change:
                    self.fields[i+1][j] = self.fields[i][j] # moves all blocks within row one row lower
