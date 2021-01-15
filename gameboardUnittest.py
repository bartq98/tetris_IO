#!/bin/env python

"""
Provides unit test of Gameboard class
Documentation about testing: https://docs.python.org/3.4/library/unittest.html


"""

import unittest

import pygame

import config
import gameboard

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






if __name__ == "__main__":
    unittest.main()