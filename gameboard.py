"""Module with Gameboard class

Gameboard class is used in main file - game.py

It is responsible for:
    - drawing board
    - holding falling tetromino (fields)
    - holding information about blocks that had fallen earlier
    - detecting which rows should be deleted (and then moving all above one block down)
"""

import pygame

import config
import drawable
import tetromino


class Gameboard(drawable.Drawable):
    """Implementing board:
        - where Tetromino falls and moves
        - where fallen Tetromino joins to board
    """

    def __init__(self):
        self.initialize_board()
        self.falling_tetromino = tetromino.Tetromino.get_random_tetromino()

    def initialize_board(self) -> None:
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

    def draw(self, screen : pygame.Surface) -> None:
        """Drawing gameboard fields (borders, empty and fallen blocks)"""

        for i, row in enumerate(self.fields):
            for j, board_elem in enumerate(row):
                self.draw_single_block(screen, board_elem, j, i)

        self.falling_tetromino.draw(screen)

    def attach_tetromino_blocks(self) -> None:
        """Attaching buffered blocks of Tetromino that has just fallen"""

        y, x = self.falling_tetromino.current_y, self.falling_tetromino.current_x

        for i, row in enumerate(self.falling_tetromino.fields):
            for j, elem in enumerate(row):
                if self.falling_tetromino.fields[i][j] == config.BUFFER_BLOCK:
                    self.fields[y + i][x + j] = config.FALLEN_BLOCK

    def generate_new_tetromino(self) -> None:
        self.falling_tetromino = tetromino.Tetromino.get_random_tetromino()

    def is_row_fully_filled(self, row : list) -> bool:
        return config.EMPTY_BLOCK not in row[config.BOARD_FIRST_COLUMN:config.BOARD_LAST_COLUMN+1]

    def delete_rows(self) -> int:
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

        return len(rows_to_detele)

    def is_tetromino_colliding(self) -> bool:
        """Return False if fields can move in specified direction, otherwise return False"""
        for i, row in enumerate(self.falling_tetromino.fields):
            for j, block in enumerate(row):
                if (self.falling_tetromino.fields[j][i] == config.BUFFER_BLOCK and
                    self.fields[self.falling_tetromino.current_y + j][self.falling_tetromino.current_x + i] in config.COLLIDING_BLOCK_TYPES):
                    return True
        return False

    def move_tetromino(self) -> None:
        """Moves bufor by pressing keys"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.falling_tetromino.change_position(event.key)
                if self.is_tetromino_colliding():
                    self.falling_tetromino.undo_change_position(event.key)

    def fall_tetromino_down(self) -> bool:
        """Moves fields one block down
        and returns True when the block collides with previously fallen blocks"""
        self.falling_tetromino.change_position(pygame.K_DOWN)
        if self.is_tetromino_colliding():
            self.falling_tetromino.undo_change_position(pygame.K_DOWN)
            return True
        else:
            return False