import time
from dataclasses import dataclass, field

import pyautogui
from PIL import ImageGrab

from utils import _infer_color, Square


@dataclass
class SquareData:
    value: str
    bomb_prob: list[float] = field(default_factory=list)
    board_index: tuple = (0, 0)

    def is_num(self):
        return self.value not in {Square.EMPTY.value, Square.UNKNOWN.value, Square.BOMB.value, Square.FLAG.value}

    def is_open(self):
        return self.is_num() or self.value == Square.EMPTY.value

    def is_flagged(self):
        return self.value == Square.FLAG.value

    def is_unknown(self):
        return self.value == Square.UNKNOWN.value

    def add_prob(self, prob):
        self.bomb_prob.append(prob)
        self.bomb_prob.sort(reverse=True)

    def get_prob(self):
        return self.bomb_prob[0] if self.bomb_prob else -1


class Board:
    def __init__(self, cols, rows, top_left_pixels, square_size, n_bombs):
        self.cols = cols
        self.rows = rows
        self.top_left_pixels = top_left_pixels
        self.square_size = square_size
        self.board = []
        self.n_flagged = 0
        self.n_bombs = n_bombs
        self.n_unknowns = 0

        for col in range(cols):
            empty_row = []
            for row in range(rows):
                empty_row.append(SquareData(value=Square.UNKNOWN.value, board_index=(col, row)))
            self.board.append(empty_row)

    def set(self, x, y, val):
            sd = SquareData(value=val.value,
                            bomb_prob=[],
                            board_index=(x, y))
            self.board[x][y] = sd

    def print_board(self):
        for row in range(self.rows):
            print("")
            for col in range(self.cols):
                print(self.board[col][row].value, end=" ")

    def get_sq_coords(self, sq: SquareData):
        x = self.top_left_pixels[0] + ((self.square_size * sq.board_index[0]) + (self.square_size / 2))
        y = self.top_left_pixels[1] + ((self.square_size * sq.board_index[1]) + (self.square_size / 2))
        return x, y

    def refresh_board(self):
        self.n_unknowns = 0

        time.sleep(0.1)
        px = ImageGrab.grab().load()
        for col in range(self.cols):
            for row in range(self.rows):
                x = self.top_left_pixels[0] + ((self.square_size * col) + (self.square_size / 2))
                y = self.top_left_pixels[1] + ((self.square_size * row) + (self.square_size / 2))
                # pyautogui.moveTo(x, y, duration=0.0)
                colors = {px[x, y], px[x+1, y+1], px[x+3, y], px[x+6, y], px[x-6, y], px[x-6, y+2], px[x-6, y-2]}
                color = _infer_color(x,y, colors, px, board_coord=(col, row))
                if color == Square.BOMB:
                    print(f"bomb detected")
                    exit()
                elif color == Square.UNKNOWN:
                    self.n_unknowns += 1
                # print(f"({col}, {row}) {colors} --> {color}")
                self.set(col, row, color)