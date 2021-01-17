#!/bin/env python

"""
Provides unit test of Gameboard class
Documentation about testing: https://docs.python.org/3.4/library/unittest.html


"""

import random
import unittest
import unittest.mock

import pygame

import config
import gameboard
import tetromino

class TestGameboardMethods(unittest.TestCase):

    # Because is hard to test Gameboard.initilize_board() method directly
    # as it is only used in __init__ (not called directly)
    # this four method below test is gameboard fields initalized properly

    def test_gameboard_fields_size(self):
        """Check if gameboad has proper size"""
        gb = gameboard.Gameboard()
        self.assertEqual(len(gb.fields), config.BOARD_ROWS) # number of rows
        for gb_row in gb.fields:
            self.assertEqual((len(gb_row)), config.BOARD_COLUMNS) # every row has blocks num

    def test_gameboard_bottom_row_is_border(self):
        """Check if gameboard bottom row is made by border type of blocks"""
        gb = gameboard.Gameboard()
        for block in gb.fields[config.BOARD_BOTTOM_ROW]:
            self.assertEqual(block, config.BORDER_BLOCK)

    def test_gameboard_max_left_column_is_border(self):
        """Check if maximum left blocks of fields are border type"""
        gb = gameboard.Gameboard()
        for block in gb.fields:
            self.assertEqual(block[0], config.BORDER_BLOCK)

    def test_gameboard_max_right_column_is_border(self):
        """Check if maximum left blocks of fields are border type"""
        gb = gameboard.Gameboard()
        for block in gb.fields:
            self.assertEqual(block[config.BOARD_COLUMNS-1], config.BORDER_BLOCK)

    # As soon as Gameboard object is created, after call draw(screen) method the screen
    # should show Gameboard on the center of screen. The coordinates of gameboard are provided by config file
    # TO BE DONE, docs for future reading:
    # https://github.com/pygame/pygame/blob/main/test/surface_test.py
    # http://www.pygame.org/docs/ref/surface.html#Surface.get_at

    def test_is_row_fully_filled(self):
        gb = gameboard.Gameboard()
        # It has no sense if bottom row is filled (it is built by BORDER_BLOCK and filled means built only by FALLEN_BLOCK)
        self.assertFalse(gb.is_row_fully_filled(gb.fields[config.BOARD_BOTTOM_ROW]))
        
        # The rest rows also should return False as new gameboard should have only empty rows (and one border at bottom)
        for row in gb.fields:
            self.assertFalse(gb.is_row_fully_filled(row))

        for index in range(config.BOARD_FIRST_COLUMN, config.BOARD_LAST_COLUMN+1):
            gb.fields[0][index] = config.FALLEN_BLOCK
        
        self.assertTrue(gb.is_row_fully_filled(gb.fields[0]))

        # Return one block to EMPTY_BLOCK to check is row not fully filled
        gb.fields[0][4] = config.EMPTY_BLOCK
        self.assertFalse(gb.is_row_fully_filled(gb.fields[0]))

        # Next row has 4 blocks filled (FALLEN_BLOCK) and rest empty
        for index in range(config.BOARD_FIRST_COLUMN, config.BOARD_LAST_COLUMN+1, 3):
            gb.fields[1][index] = config.FALLEN_BLOCK

        self.assertFalse(gb.is_row_fully_filled(gb.fields[1]))

        # This row has only one block FALLEN
        gb.fields[2][1] = config.FALLEN_BLOCK
        self.assertFalse(gb.is_row_fully_filled(gb.fields[2]))


    def test_generate_new_tetromino(self):
        # Every time the Tetromino itself is diffrent this method should return diffrent value
        gb = gameboard.Gameboard()
        # gb.generate_new_tetromino = unittest.mock.MagicMock(return_value=tetromino.Tetromino("I"))

        # TODO Check if every call gives properly placed tetromino
        for shape in config.TETROMINO_SHAPES:
            for rotate in range(0, 3):
                gb.generate_new_tetromino = unittest.mock.MagicMock(return_value=tetromino.Tetromino(shape, rotate))
                self.assertEqual(type(gb.falling_tetromino), tetromino.Tetromino)

    # Do is_tetromino_colliding można dodać sprawdzanie, czy dalej jest na planszy :)))

    def test_attach_tetromino_blocks(self):
        """Check if Tetromino is properly attached to board"""

        def check_if_attached_properly(gb: gameboard.Gameboard):
            """Check if for currently state of gameboard call attach_tetromino_blocks will attach blocks properly"""

            gb.attach_tetromino_blocks()
            x, y = gb.falling_tetromino.current_x, gb.falling_tetromino.current_y

            for y_shift, row in enumerate(gb.falling_tetromino.fields):
                for x_shift, block in enumerate(row):
                    if block == config.BUFFER_BLOCK: # checks only Tetromino BUFFER_BLOCKS (only these are attached)
                        self.assertEqual(gb.fields[y + y_shift][x + x_shift], config.FALLEN_BLOCK)

        # Case for Tetromino on initial position
        gb = gameboard.Gameboard()
        check_if_attached_properly(gb)

        # Case for Tetromino moved three times down
        gb = gameboard.Gameboard()
        for _ in range(3):
            gb.fall_tetromino_down()
        check_if_attached_properly(gb)

        # Case for Tetromino moved one time down, rotated and then shifted three times right
        gb = gameboard.Gameboard()
        gb.fall_tetromino_down()
        gb.falling_tetromino.rotate()
        gb.falling_tetromino.current_x += 3
        check_if_attached_properly(gb)

    def test_delete_rows(self):
        """Check if delete rows returns proper quantity of deleted rows and the Gameboard has proper fields after deletion"""

        def fill_row_no(gb : gameboard.Gameboard, row_no : int):
            for i in range(config.BOARD_FIRST_COLUMN, config.BOARD_LAST_COLUMN+1):
                gb.fields[row_no][i] = config.FALLEN_BLOCK


        gb = gameboard.Gameboard()
        # If gameboard is new (and empty) there are no empty rows to delete
        self.assertEqual(gb.delete_rows(), 0)

        fill_row_no(gb, 0)
        fill_row_no(gb, 1)
        fill_row_no(gb, 2)
        fill_row_no(gb, 3)
        fill_row_no(gb, 4)
        fill_row_no(gb, 5)
        fill_row_no(gb, 6)

        self.assertEqual(gb.delete_rows(), 7)
        self.assertEqual(gb.delete_rows(), 0) # After deletion there must not be any filled row

        fill_row_no(gb, 0)
        gb.fields[0][3] = config.EMPTY_BLOCK # Almost fully filled row (except third block)
        self.assertEqual(gb.delete_rows(), 0)

        # Check if positions of blocks after deletion and moving down are proper
        fill_row_no(gb, config.BOARD_LAST_ROW)
        fill_row_no(gb, config.BOARD_LAST_ROW-1)

        row_to_check1, row_to_check2 = 6, 2
        col_to_check1, col_to_check2 = 3, 8
        gb.fields[row_to_check1][col_to_check1] = config.FALLEN_BLOCK
        gb.fields[row_to_check2][col_to_check2] = config.FALLEN_BLOCK
        self.assertEqual(gb.delete_rows(), 2)

        self.assertEqual(gb.fields[row_to_check1][col_to_check1], config.EMPTY_BLOCK) # Blocks should be empty
        self.assertEqual(gb.fields[row_to_check2][col_to_check2], config.EMPTY_BLOCK)
        self.assertEqual(gb.fields[row_to_check1+2][col_to_check1], config.FALLEN_BLOCK) # There was two deleted rows so blocks moved two rows down
        self.assertEqual(gb.fields[row_to_check1+2][col_to_check1], config.FALLEN_BLOCK)

    def test_is_tetromino_colliding(self):

        gb = gameboard.Gameboard()
        self.assertEqual(gb.is_tetromino_colliding(), False)

        # Test for borders

        gb.falling_tetromino = tetromino.Tetromino("I", times_rotated=1, x=0)
        # for "I" shape, the most left block will overlaping with gameboard left border
        self.assertEqual(gb.is_tetromino_colliding(), True)

        gb.falling_tetromino = tetromino.Tetromino("I", times_rotated=1, x=config.BOARD_COLUMNS-4)
        self.assertEqual(gb.is_tetromino_colliding(), True)

        # for bottom row (border)
        gb.falling_tetromino = tetromino.Tetromino("Z", x=4, y=config.BOARD_ROWS-3)
        self.assertEqual(gb.is_tetromino_colliding(), True)

        # Test for some FALLEN BLOCKS

        gb.falling_tetromino = tetromino.Tetromino("Z", x=8, y=4)
        gb.fields[8][3] = config.FALLEN_BLOCK
        gb.fields[8][4] = config.FALLEN_BLOCK
        gb.fields[8][5] = config.FALLEN_BLOCK
        gb.fields[7][3] = config.FALLEN_BLOCK
        self.assertEqual(gb.is_tetromino_colliding(), True)

        # Check for changing single block from FALLEN to EMPTY (block witch causing collision)
        gb = gameboard.Gameboard()
        gb.falling_tetromino = tetromino.Tetromino("O", x=0, y=0)
        gb.fields[1][2] = config.FALLEN_BLOCK
        self.assertEqual(gb.is_tetromino_colliding(), True)
        gb.fields[1][2] = config.EMPTY_BLOCK
        self.assertEqual(gb.is_tetromino_colliding(), False)



if __name__ == "__main__":
    unittest.main()
    print(f"Every test of Gameboard class has passed")