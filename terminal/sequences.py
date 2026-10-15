
"""ANSI escape sequences for terminal control."""

from .colors import Color
from .font_styles import FontStyle

ESC = "\033"
CSI = f"{ESC}["

#  Screen and line control
CLEAR_SCREEN = f"{CSI}2J"
CLEAR_LINE = f"{CSI}2K"

#  Cursor positioning
CURSOR_HOME = f"{CSI}H"
CURSOR_POSITION = f"{CSI}{{row}};{{column}}H"

#  Cursor visibility
CURSOR_HIDE = f"{CSI}?25l"
CURSOR_SHOW = f"{CSI}?25h"

RESET_ATTRIBUTES = f"{CSI}0m"

#  available colors
FOREGROUND_COLORS = {
    Color.BLACK: 30,
    Color.RED: 31,
    Color.GREEN: 32,
    Color.YELLOW: 33,
    Color.BLUE: 34,
    Color.MAGENTA: 35,
    Color.CYAN: 36,
    Color.WHITE: 37,
    Color.BRIGHT_BLACK: 90,
    Color.BRIGHT_RED: 91,
    Color.BRIGHT_GREEN: 92,
    Color.BRIGHT_YELLOW: 93,
    Color.BRIGHT_BLUE: 94,
    Color.BRIGHT_MAGENTA: 95,
    Color.BRIGHT_CYAN: 96,
    Color.BRIGHT_WHITE: 97,
}

BACKGROUND_COLORS = {
    Color.BLACK: 40,
    Color.RED: 41,
    Color.GREEN: 42,
    Color.YELLOW: 43,
    Color.BLUE: 44,
    Color.MAGENTA: 45,
    Color.CYAN: 46,
    Color.WHITE: 47,
    Color.BRIGHT_BLACK: 100,
    Color.BRIGHT_RED: 101,
    Color.BRIGHT_GREEN: 102,
    Color.BRIGHT_YELLOW: 103,
    Color.BRIGHT_BLUE: 104,
    Color.BRIGHT_MAGENTA: 105,
    Color.BRIGHT_CYAN: 106,
    Color.BRIGHT_WHITE: 107,
}

FONT_STYLES = {
    FontStyle.BOLD: 1,
    FontStyle.DIM: 2,
    FontStyle.ITALIC: 3,
    FontStyle.UNDERLINE: 4,
    FontStyle.BLINK: 5,
    FontStyle.REVERSE: 7,
    FontStyle.HIDDEN: 8,
    FontStyle.STRIKETHROUGH: 9
}

FONT_RESETS = {
    FontStyle.BOLD: 22,
    FontStyle.DIM: 22,
    FontStyle.ITALIC: 23,
    FontStyle.UNDERLINE: 24,
    FontStyle.BLINK: 25,
    FontStyle.REVERSE: 27,
    FontStyle.HIDDEN: 28,
    FontStyle.STRIKETHROUGH: 29
}
