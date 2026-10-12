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

    UNKNOWN = enum.auto()

class Modifier(enum.Enum):
    CTRL = enum.auto()
    ALT = enum.auto()
    SHIFT = enum.auto()


KEY_SEQUENCES: dict[str, Key] = {
    # Escape
    "\033": Key.ESCAPE,

    # Arrow keys
    "\033[A": Key.UP,
    "\033[B": Key.DOWN,
    "\033[C": Key.RIGHT,
    "\033[D": Key.LEFT,

    # Arrow keys: application mode (SS3)
    "\033OA": Key.UP,
    "\033OB": Key.DOWN,
    "\033OC": Key.RIGHT,
    "\033OD": Key.LEFT,

    # Home and End
    "\033[H": Key.HOME,
    "\033[F": Key.END,

    "\033OH": Key.HOME,
    "\033OF": Key.END,

    "\033[1~": Key.HOME,
    "\033[4~": Key.END,

    "\033[7~": Key.HOME,
    "\033[8~": Key.END,

    # Insert, Delete, Page Up, Page Down
    "\033[2~": Key.INSERT,
    "\033[3~": Key.DELETE,
    "\033[5~": Key.PAGE_UP,
    "\033[6~": Key.PAGE_DOWN,

    # Function keys F1-F4: SS3
    "\033OP": Key.F1,
    "\033OQ": Key.F2,
    "\033OR": Key.F3,
    "\033OS": Key.F4,

    # Function keys F1-F4: CSI
    "\033[11~": Key.F1,
    "\033[12~": Key.F2,
    "\033[13~": Key.F3,
    "\033[14~": Key.F4,

    # Function keys F5-F12
    "\033[15~": Key.F5,
    "\033[17~": Key.F6,
    "\033[18~": Key.F7,
    "\033[19~": Key.F8,
    "\033[20~": Key.F9,
    "\033[21~": Key.F10,
    "\033[23~": Key.F11,
    "\033[24~": Key.F12,

    # Control characters
    "\r": Key.ENTER,
    "\n": Key.ENTER,
    "\t": Key.TAB,
    "\x7f": Key.BACKSPACE,
    "\x08": Key.BACKSPACE,
}


@dataclasses.dataclass(frozen=True)
class KeyPress:
    key: Key | None = None
    unicode: str | None = None
    modifiers: frozenset[Modifier] = frozenset()

    def __post_init__(self) -> None:
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
        if not isinstance(self.modifiers, frozenset):
            raise TypeError(
                "modifiers must be a frozenset."
            )
        if not all(isinstance(m, Modifier) for m in self.modifiers):
            raise TypeError(
                "all modifiers must be instances of Modifier."
            )
