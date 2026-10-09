"""ANSI escape sequences for terminal control."""

ESC = "\033"
CSI = f"{ESC}["

# Screen and line control
CLEAR_SCREEN = f"{CSI}2J"
CLEAR_LINE = f"{CSI}2K"

# Cursor positioning
CURSOR_HOME = f"{CSI}H"
CURSOR_POSITION = f"{CSI}{{row}};{{column}}H"

# Cursor visibility
CURSOR_HIDE = f"{CSI}?25l"
CURSOR_SHOW = f"{CSI}?25h"
