# TETRIS

A simple clone of [**Tetris**](https://www.youtube.com/watch?v=pn0__1N9ykE) (1989 NES version) written in Python and Pygame.

## General info

This project is based on my previous [repository](https://github.com/bartq98/tetris) (I also encourage you to discover it!). Unlike that version, this version selects shape of Tetromino at random.

Other improvments:
- main menu
- code fixes and general refacor

This project is implemented as part of the Software Engineering Course at Cracow Univeristy of Technology.

Ten projekt jest realizowany w ramach przedmiotu **Inżynieria Oprogramowania** na Politechice Krakowskiej.

## Setup

This game was develop and tested on Manjaro Linux. It also should working well on OSX or Windows.

To run game, firstly make sure you have Python 3 (and pip) installed on your computer.

```
git clone https://github.com/bartq98/tetris_IO
cd tetris_IO
pip install requirements.txt
python ./game.py
```


## How to play?
You can control falling tetromino as in the classic NES version:

|Arrow|Action|
|:-:	|:-:	|
| ↑ 	| rotates tetromino clockwise 	|
| ↓ 	| speeds up falling down 	|
| → 	| moves left 	|
| ← 	| moves right 	|



