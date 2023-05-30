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
    SEVEN = "7"
    EIGHT = "8"

# pyautogui.moveTo(506.0, 438.0, duration=1)
# pyautogui.moveTo(507.0, 469.0, duration=1)


def _empty_or_unopened(x, y, px):
    # white (250, 250, 250) or grey (166, 166, 166) boarder

    color = px[x, y]
    while color[0] == 198 or color[0] == 189:  # search lower pixes until one isn't grey:
        y -= 1
        color = px[x, y]
    # print(f"empty-or-unopened ? ({x},{y}) = {color}")
    return Square.UNKNOWN if color == (250, 250, 250) or color == (255, 255, 255) or color == (134, 134, 134) \
                            or color == (207, 207, 207) or color == (199, 199, 199) else Square.EMPTY


def _is_flag(colors):
    # A Flag has a few shades of RED
    for color in colors:
        if color[0] - 130 > color[1] and color[0] - 130 > color[2]:  # Red in RGB much more significant than others
            print(f"is flag!")
            return True
    return False


def _is_green(colors):
    for color in colors:
        if color[1] - 100 > color[0] and color[1] - 100 > color[2]:
            return True
    return False


def _infer_square(x, y, colors: set, px, board_coord: tuple):
    if (0, 0, 255) in colors:
        return Square.ONE
    elif _is_green(colors):
        return Square.TWO
    elif (255, 0, 0) in colors and (0, 0, 0) not in colors:
        return Square.THREE
    elif (0, 0, 128) in colors or (0, 0, 123) in colors:
        return Square.FOUR
    elif (128, 0, 0) in colors or (123, 0, 0) in colors:
        return Square.FIVE
    elif (0, 123, 123) in colors or (0, 128, 128) in colors:
        return Square.SIX
    # elif (123, 123, 123) in colors or (128, 128, 128) in colors:
    #     return Square.EIGHT
    elif ((0, 0, 0) in colors and (255, 0, 0) in colors) or (26, 17, 17) in colors or (95, 77, 77) in colors or _is_flag(colors):
        return Square.FLAG
    elif (222, 221, 221) in colors or (222, 220, 220) in colors or (0, 0, 0) in colors:
        return Square.BOMB
    elif all([a == (198, 198, 198) for a in colors]) or (189, 189, 189) in colors:
        return _empty_or_unopened(x, y, px)

    print(f"couldn't find color for board-coord: ({board_coord}) ({x},{y}) - {colors}")