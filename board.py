import time
from dataclasses import dataclass, field

import pyautogui
from PIL import ImageGrab

from utils import _infer_square, Square


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
    def __init__(self, cols, rows, top_left_pixels, square_size, n_bombs, offset):
        self.cols = cols
        self.rows = rows
        self.top_left_pixels = top_left_pixels
        self.square_size = square_size
        self.board = []
        self.n_flagged = 0
        self.n_bombs = n_bombs
        self.n_unknowns = 0
        self.offset = offset

        # Init self.board with empty unknown arrays
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
        print("")

    def get_sq_coords(self, sq: SquareData):
        x = self.top_left_pixels[0] + (((self.square_size - 0.5) * sq.board_index[0]) + (self.square_size / 2))
        y = self.top_left_pixels[1] + ((self.square_size * sq.board_index[1]) + (self.square_size / 2))
        return x, y

    def _get_surrounding_pixels(self, px, x, y):
        res = {px[x, y]}
        for i in range(int((self.square_size/2) - 1)):
            for j in range(int((self.square_size / 2) - 1)):
                res.add(px[x + i, y + j])
                res.add(px[x - i, y + j])
                res.add(px[x + i, y - j])
                res.add(px[x - i, y - j])
        return res

    def refresh_board(self, debug=False):
        self.n_unknowns = 0

        time.sleep(0.1)
        px = ImageGrab.grab().load()
        for col in range(self.cols):
            for row in range(self.rows):
                x = self.top_left_pixels[0] + (((self.square_size-self.offset) * col) + (self.square_size / 2))
                y = self.top_left_pixels[1] + ((self.square_size * row) + (self.square_size / 2))
                if debug:
                    pyautogui.moveTo(x, y, duration=0.0)
                surrounding_colors = self._get_surrounding_pixels(px, x, y)
                sq = _infer_square(x, y, surrounding_colors, px, board_coord=(col, row))
                print(f"({col}, {row}) from colors {surrounding_colors} inferred --> {sq}")
                if sq == Square.BOMB:
                    print(f"bomb detected")
                    if not debug:
                        exit()
                elif sq == Square.UNKNOWN:
                    self.n_unknowns += 1
                # print(f"({col}, {row}) {colors} --> {color}")
                self.set(col, row, sq)
