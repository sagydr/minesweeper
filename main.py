import random
from dataclasses import dataclass

import pyautogui
# import ImageGrab
# import Pillow
from PIL import ImageGrab
from board import Board
from utils import Square

# https://minesweeper.online

square_size = 24


@dataclass
class Beginner:
    top_left = (735, 327.5)
    board_size = (9, 9)
    n_bombs = 10


@dataclass
class Expert:
    top_left = (703, 325)
    board_size = (30, 16)
    n_bombs = 99
# pyautogui.moveTo(705, 330, duration = 1)

px = ImageGrab.grab().load()


def find_unknown_neighbors(square, board):
    cols, rows = len(board), len(board[0])
    col, row = square.board_index[0], square.board_index[1]
    neighbors = [
        board[j][i]
        for i in range(row - 1, row + 2)
        for j in range(col - 1, col + 2)
        if 0 <= i < rows and 0 <= j < cols and (i != row or j != col)
    ]
    return [n for n in neighbors if n.is_unknown()], [n for n in neighbors if n.is_flagged()], [n for n in neighbors if n.is_num()]


def calc_probs(board):
    marked_bombs = 0
    for col in range(board.cols):
        for row in range(board.rows):
            sq = board.board[col][row]

            if sq.is_num():
                unknown_neigh, flagged_neigh, _ = find_unknown_neighbors(square=sq, board=board.board)
                if not unknown_neigh:
                    continue

                num_bombs = int(sq.value) - len(flagged_neigh)  # reduce already marked bombs
                if num_bombs == 0:
                    # open neighbors since all bombs were marked
                    for unknown_sq in unknown_neigh:
                        x, y = board.get_sq_coords(unknown_sq)
                        pyautogui.leftClick(x=x, y=y)
                else:
                    # print(f"open_neihbors ({sq}) = {unknown_neigh}")
                    prob_per_square = num_bombs / len(unknown_neigh)
                    for neighbor in unknown_neigh:
                        if prob_per_square == 1:
                            _mark_bomb(board=board, sq=neighbor)
                            marked_bombs += 1
                        else:
                            neighbor.add_prob(prob_per_square)
                            print(f"{neighbor} -- prob = {prob_per_square}")


def _mark_bomb(board, sq):
    print(f"marking bomb at {sq.board_index}")
    x, y = board.get_sq_coords(sq)
    pyautogui.rightClick(x=x, y=y)
    board.set(x=sq.board_index[0], y=sq.board_index[1], val=Square.FLAG)
    board.n_flagged += 1


def mark_bombs(board, thresh=0.9):
    flagged = []
    for col in range(board.cols):
        for row in range(board.rows):
            sq = board.board[col][row]
            if sq.is_num():
                unknown_neigh, flagged_neigh, _ = find_unknown_neighbors(square=sq, board=board.board)
                unknowns_sorted = [(unknown_sq.get_prob(), unknown_sq) for unknown_sq in unknown_neigh]
                if not unknowns_sorted:
                    continue
                print(f"({sq}) --- {unknowns_sorted=} --- {flagged_neigh=}")
                unknowns_sorted.sort(key=lambda x: x[0])
                top_prob, top_unknown = unknowns_sorted[0]

                if top_prob >= thresh:
                    _mark_bomb(board, sq=top_unknown)
                    flagged.append(top_unknown)
                    print(f"setting board[{col}][{row}] = {Square.FLAG}")
                    board.print_board()
    return flagged


def middle_click_flagged_neighbors(board, flagged):
    clicks = 0
    for flagged_sq in flagged:
        _, _, num_neighbors = find_unknown_neighbors(square=flagged_sq, board=board.board)
        for num_sq in num_neighbors:
            x, y = board.get_sq_coords(num_sq)
            pyautogui.middleClick(x=x, y=y)
            clicks += 1
    print(f"pressed {clicks} double-clicks on numbers")


def _get_all_unknowns(board):
    unknowns = []
    for col in range(board.cols):
        for row in range(board.rows):
            sq = board.board[col][row]
            if sq.value == Square.UNKNOWN.value:
                unknowns.append(sq)
    return unknowns


def random_open_a_square(board):
    global px
    all_unknown_squares = _get_all_unknowns(board)
    sq = random.choice(all_unknown_squares)
    print(f"opening a random square: {sq}")
    x, y = board.get_sq_coords(sq)
    pyautogui.leftClick(x=x, y=y)
    px = ImageGrab.grab().load()


def open_four_corners(board):
    global px
    for sq in [board.board[0][0], board.board[0][board.rows - 1],
               board.board[board.cols - 1][board.rows - 1], board.board[board.cols - 1][0]]:
        x, y = board.get_sq_coords(sq)
        pyautogui.leftClick(x=x, y=y)
        px = ImageGrab.grab().load()


def is_game_over(board):
    # return board.n_bombs == board.n_flagged
    print(f"n_bombs = {board.n_bombs} , n_flagged = {board.n_flagged} --> is over? {board.n_bombs == board.n_flagged}")
    return board.n_bombs == board.n_flagged


def main(board_level):
    pyautogui.moveTo(board_level.top_left[0], board_level.top_left[1], duration=1)
    board = Board(cols=board_level.board_size[0], rows=board_level.board_size[1],
                  top_left_pixels=board_level.top_left, square_size=square_size, n_bombs=board_level.n_bombs)
    # random_open_a_square(board)
    open_four_corners(board)

    while not is_game_over(board):
        flagged = []
        thresh = 0.9
        board.refresh_board()
        board.print_board()
        print("calculating probabilities")
        marked_bombs = calc_probs(board=board)
        if marked_bombs:
            board.refresh_board()
            board.print_board()

        while len(flagged) == 0 and thresh >= 0.5:
            non_bomb_prob = (board.n_bombs - board.n_flagged) / board.n_unknowns
            print(f"({board.n_bombs} - {board.n_flagged}) / {board.n_unknowns} = {non_bomb_prob=}")

            flagged = mark_bombs(board=board, thresh=thresh)
            print(f"marked {len(flagged)} new flags when thresh is {thresh}")
            thresh -= 0.2

        if len(flagged) == 0:
            random_open_a_square(board=board)
        else:
            middle_click_flagged_neighbors(board=board, flagged=flagged)


if __name__ == '__main__':
    # main(board_level=Beginner)
    main(board_level=Expert)
