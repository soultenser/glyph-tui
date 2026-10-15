
"""Keyboard key definitions and parsed key press values."""

import dataclasses
import enum


class Key(enum.Enum):
    """Enumeration of supported terminal keys and special inputs."""

    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    HOME = enum.auto()
    END = enum.auto()
    PAGE_UP = enum.auto()
    PAGE_DOWN = enum.auto()
    INSERT = enum.auto()
    DELETE = enum.auto()

    ENTER = enum.auto()
    ESCAPE = enum.auto()
    BACKSPACE = enum.auto()
    TAB = enum.auto()

    F1 = enum.auto()
    F2 = enum.auto()
    F3 = enum.auto()
    F4 = enum.auto()
    F5 = enum.auto()
    F6 = enum.auto()
    F7 = enum.auto()
    F8 = enum.auto()
    F9 = enum.auto()
    F10 = enum.auto()
    F11 = enum.auto()
    F12 = enum.auto()

    UNKNOWN = enum.auto()


@dataclasses.dataclass(frozen=True)
class KeyPress:
    """Represents a single terminal key press.

    Exactly one of ``key`` or ``unicode`` must be provided.
    """

    key: Key | None = None
    unicode: str | None = None

    def __post_init__(self) -> None:
        """Validate the key press fields and value constraints.

        Raises:
            ValueError: If both or neither of ``key`` and ``unicode`` are set,
                or a Unicode character is not exactly one code point long.
            TypeError: If any field has an unsupported type.
        """
        if (self.key is None) == (self.unicode is None):
            raise ValueError(
                "exactly one of 'key' or 'unicode' must be provided."
            )
        if self.key is not None and not isinstance(self.key, Key):
            raise TypeError(
                "key must be an instance of Key or None."
            )
        if self.unicode is not None:
            if not isinstance(self.unicode, str):
                raise TypeError(
                    "unicode must be a string or None."
                )
            if len(self.unicode) != 1:
                raise ValueError(
                    "unicode must contain exactly one character."
                )
