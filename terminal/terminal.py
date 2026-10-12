
import select
import shutil
import sys
import termios
import tty

from .colors import Color
from .keys import (
    Key,
    KEY_SEQUENCES,
    KeyPress,
)
from .sequences import (
    BACKGROUND_COLORS,
    CLEAR_LINE,
    CLEAR_SCREEN,
    CSI,
    CURSOR_HOME,
    CURSOR_HIDE,
    CURSOR_POSITION,
    CURSOR_SHOW,
    FOREGROUND_COLORS,
    RESET_ATTRIBUTES,
)


class TerminalError(Exception):
    ...


class Terminal:

    def __init__(self) -> None:
        self.state: termios._AttrReturn | None = None
        self.valid_sequences: set[str] = set(KEY_SEQUENCES.keys())

    #  basic functionalities
    def write(self, text: str) -> None:
        sys.stdout.write(text)

    def flush(self) -> None:
        sys.stdout.flush()

    def move_cursor(self, position: tuple[int, int]) -> None:
        if not isinstance(position, tuple):
            raise TypeError(
                "position must be a tuple."
            )
        if len(position) != 2:
            raise ValueError(
                "position must contain exactly two coordinates."
            )

        x, y = position
        if type(x) is not int or type(y) is not int:
            raise TypeError(
                "coordinates must be integers."
            )
        if x < 0 or y < 0:
            raise ValueError(
                "coordinates must be non-negative integers."
            )

        sequence = CURSOR_POSITION.format(row=y + 1, column=x + 1)
        sys.stdout.write(sequence)

    def move_cursor_home(self) -> None:
        sys.stdout.write(CURSOR_HOME)

    def clear_screen(self) -> None:
        sys.stdout.write(CLEAR_SCREEN)

    def clear_line(self) -> None:
        sys.stdout.write(CLEAR_LINE)

    def set_cursor_visible(self, visible: bool = True) -> None:
        if not isinstance(visible, bool):
            raise TypeError(
                "visible must be a boolean."
            )

        sequence = CURSOR_SHOW if visible else CURSOR_HIDE
        sys.stdout.write(sequence)

    def get_size(self) -> tuple[int, int]:
        size = shutil.get_terminal_size()
        return (size.columns, size.lines)

    def reset_attributes(self) -> None:
        sys.stdout.write(RESET_ATTRIBUTES)

    #  color management
    def __get_color_sequence(
        self,
        color: Color | tuple[int, int, int],
        foreground: bool,
    ) -> str:
        if isinstance(color, Color):
            colors = FOREGROUND_COLORS if foreground else BACKGROUND_COLORS
            return f"{CSI}{colors[color]}m"

        if not isinstance(color, tuple):
            raise TypeError(
                "Color must be a Color or an RGB tuple."
            )

        if len(color) != 3:
            raise ValueError(
                "RGB color must contain exactly three components."
            )

        if any(type(component) is not int for component in color):
            raise TypeError(
                "RGB components must be integers."
            )

        if any(not 0 <= component <= 255 for component in color):
            raise ValueError(
                "RGB components must be between 0 and 255."
            )

        code = 38 if foreground else 48
        red, green, blue = color

        return f"{CSI}{code};2;{red};{green};{blue}m"

    def set_foreground_color(
        self,
        color: Color | tuple[int, int, int]
    ) -> None:

        sequence = self.__get_color_sequence(
            color=color, foreground=True
        )
        sys.stdout.write(sequence)

    def set_background_color(
        self,
        color: Color | tuple[int, int, int]
    ) -> None:

        sequence = self.__get_color_sequence(
            color=color, foreground=False
        )
        sys.stdout.write(sequence)

    def set_color(
        self,
        foreground: Color | tuple[int, int, int] | None = None,
        background: Color | tuple[int, int, int] | None = None,
    ) -> None:

        if foreground is not None:
            self.set_foreground_color(color=foreground)
        if background is not None:
            self.set_background_color(color=background)

    #  getting keyboard inputs
    def raw(self) -> None:
        fd = sys.stdin.fileno()
        if self.state is None:
            self.state = termios.tcgetattr(fd)
            tty.setraw(fd)

    def restore(self) -> None:
        if self.state is not None:
            termios.tcsetattr(
                sys.stdin.fileno(), termios.TCSADRAIN, self.state
            )
            self.state = None

    def __get_escape_sequence(self) -> str | None:
        sequence = "\033"
        while True:
            if not any(s.startswith(sequence) for s in self.valid_sequences):
                break

            ready, _, _ = select.select([sys.stdin], [], [], 0.05)

            if not ready:
                break
            nextchar = sys.stdin.read(1)
            if not nextchar:
                break
            sequence += nextchar

        return sequence if sequence in self.valid_sequences else None

    def getch(self) -> KeyPress:
        self.raw()

        try:
            char = sys.stdin.read(1)
            if char == "":
                raise TerminalError(
                    "unexpected end of input (EOF)."
                )
            if char != "\033":
                key = KEY_SEQUENCES.get(char, None)
                if key is None:
                    return KeyPress(unicode=char)
                return KeyPress(key=key)

            sequence = self.__get_escape_sequence()
        except Exception:
            self.restore()
            raise

        key = KEY_SEQUENCES.get(sequence, None)
        if key is None:
            return KeyPress(key=Key.UNKNOWN)
        return KeyPress(key=key)

    def getch_nowait(self) -> KeyPress | None:
        pass
