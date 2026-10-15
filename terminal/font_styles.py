
"""Supported terminal font styles used for ANSI text formatting."""

import enum


class FontStyle(enum.Enum):
    """Terminal text styles recognized by the ANSI escape sequences."""

    BOLD = enum.auto()
    DIM = enum.auto()
    ITALIC = enum.auto()
    UNDERLINE = enum.auto()
    BLINK = enum.auto()
    REVERSE = enum.auto()
    HIDDEN = enum.auto()
    STRIKETHROUGH = enum.auto()
