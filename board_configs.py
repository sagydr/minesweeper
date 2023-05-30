from dataclasses import dataclass


@dataclass
class Beginner:
    # https://minesweeper.online
    top_left = (735, 327.5)
    board_size = (9, 9)
    n_bombs = 10
    offset = 0


@dataclass
class Expert:
    # https://minesweeper.online
    top_left = (703, 325)
    board_size = (30, 16)
    n_bombs = 99
    square_size = 24
    offset = 0


@dataclass
class BeginnerMinesweeperOnline:
    # https://minesweeperonline.com
    top_left = (507, 191)
    board_size = (9, 9)
    n_bombs = 10
    square_size = 18
    offset = 0


@dataclass
class ExpertMinesweeperOnline:
    # https://minesweeperonline.com
    top_left = (498, 190)
    board_size = (30, 16)
    n_bombs = 99
    square_size = 18
    offset = 0.5