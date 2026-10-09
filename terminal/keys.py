import enum
import dataclasses


class Key(enum.Enum):
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


class Modifier(enum.Enum):
    CTRL = enum.auto()
    ALT = enum.auto()
    SHIFT = enum.auto()


@dataclasses.dataclass(frozen=True)
class KeyPress:
    key: Key | None = None
    char: str | None = None
    modifiers: frozenset[Modifier] = frozenset()

    def __post_init__(self) -> None:
        if (self.key is None) == (self.char is None):
            raise ValueError(
                "exactly one of 'key' or 'char' must be provided."
            )
        if self.key is not None and not isinstance(self.key, Key):
            raise TypeError(
                "key must be an instance of Key or None."
            )
        if self.char is not None:
            if not isinstance(self.char, str):
                raise TypeError(
                    "char must be a string or None."
                )
            if len(self.char) != 1:
                raise ValueError(
                    "char must contain exactly one character."
                )
        if not isinstance(self.modifiers, frozenset):
            raise TypeError(
                "modifiers must be a frozenset."
            )
        if not all(isinstance(m, Modifier) for m in self.modifiers):
            raise TypeError(
                "all modifiers must be instances of Modifier."
            )
