from enum import Enum

import pyautogui


class Square(Enum):
    EMPTY = "_"
    UNKNOWN = "?"
    BOMB = "*"
    FLAG = "F"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"

pyautogui.moveTo(x=700, y=330)


def _empty_or_unopened(x, y, px):
    # white (250, 250, 250) or grey (166, 166, 166) boarder

    color = px[x, y]
    while color[0] == 198:  # search lower pixes until one isn't grey:
        y += 1
        color = px[x, y]
    # print(f"empty-or-unopened ? ({x},{y}) = {color}")
    return Square.UNKNOWN if color == (250, 250, 250) or color == (134, 134, 134) else Square.EMPTY


def _is_flag(colors):
    # A Flag has a few shades of RED
    for color in colors:
        if color[0] - 130 > color[1] and color[0] - 130 > color[2]:  # Red in RGB much more significant than others
            print(f"is flag!")
            return True


def _infer_color(x, y, colors: set, px, board_coord: tuple):
    if (0, 0, 255) in colors:
        return Square.ONE
    elif (0, 128, 0) in colors:
        return Square.TWO
    elif (255, 0, 0) in colors:
        return Square.THREE
    elif (0, 0, 128) in colors:
        return Square.FOUR
    elif (128, 0, 0) in colors:
        return Square.FIVE
    elif (26, 17, 17) in colors or (95, 77, 77) in colors or _is_flag(colors):
        return Square.FLAG
    elif (222, 221, 221) in colors or (222, 220, 220) in colors:
        return Square.BOMB
    elif all([a == (198, 198, 198) for a in colors]):
        return _empty_or_unopened(x, y, px)

    print(f"couldn't find color for board-coord: ({board_coord}) ({x},{y}) - {colors}")