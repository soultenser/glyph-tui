
"""Terminal utilities for ANSI output and raw keyboard input."""

import select
import shutil
import sys
import termios
import tty

from .colors import Color
from .font_styles import FontStyle
from .keys import (
    Key,
    KeyPress,
)
from .key_sequences import KEY_SEQUENCES
from .sequences import (
    BACKGROUND_COLORS,
    CLEAR_LINE,
    CLEAR_SCREEN,
    CSI,
    CURSOR_HOME,
    CURSOR_HIDE,
    CURSOR_POSITION,
    CURSOR_SHOW,
    FONT_RESETS,
    FONT_STYLES,
    FOREGROUND_COLORS,
    RESET_ATTRIBUTES,
)


class TerminalError(Exception):
    """Raised when terminal input cannot be a valid key sequence."""


class Terminal:
    """Manage terminal output and keyboard input for interactive applications.

    The class wraps ANSI escape codes for cursor movement, screen control,
    styling, and raw read operations used by TUI programs.
    """

    def __init__(self) -> None:
        """Initialize terminal state and the set of known escape sequences."""
        self.state: termios._AttrReturn | None = None
        self.valid_sequences: set[str] = set(KEY_SEQUENCES.keys())

    #  basic functionalities
    def write(self, text: str) -> None:
        """Write text to standard output.

        Args:
            text: The text to emit to stdout.
        """
        sys.stdout.write(text)

    def flush(self) -> None:
        """Flush standard output."""
        sys.stdout.flush()

    def move_cursor(self, position: tuple[int, int]) -> None:
        """Move the cursor to a terminal coordinate.

        Args:
            position: An ``(x, y)`` tuple describing the target cell.

        Raises:
            TypeError: If the position is not a tuple or contains non-integer
                coordinates.
            ValueError: If the tuple does not contain exactly two coordinates
                or any coordinate is negative.
        """
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
        """Move the cursor to the home position."""
        sys.stdout.write(CURSOR_HOME)

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        sys.stdout.write(CLEAR_SCREEN)

    def clear_line(self) -> None:
        """Clear the current terminal line."""
        sys.stdout.write(CLEAR_LINE)

    def set_cursor_visible(self, visible: bool = True) -> None:
        """Show or hide the terminal cursor.

        Args:
            visible: Whether the cursor should be visible.

        Raises:
            TypeError: If ``visible`` is not a boolean.
        """
        if not isinstance(visible, bool):
            raise TypeError(
                "visible must be a boolean."
            )

        sequence = CURSOR_SHOW if visible else CURSOR_HIDE
        sys.stdout.write(sequence)

    def get_size(self) -> tuple[int, int]:
        """Return the current terminal size as ``(columns, rows)``.

        Returns:
            A tuple containing the terminal width and height.
        """
        size = shutil.get_terminal_size()
        return (size.columns, size.lines)

    def reset_attributes(self) -> None:
        """Reset any active terminal text attributes."""
        sys.stdout.write(RESET_ATTRIBUTES)

    #  getting keyboard inputs
    def raw(self) -> None:
        """Enable raw terminal mode for direct keyboard reads."""
        fd = sys.stdin.fileno()
        if self.state is None:
            self.state = termios.tcgetattr(fd)
            tty.setraw(fd)

    def restore(self) -> None:
        """Restore the prior terminal settings after raw mode."""
        if self.state is not None:
            termios.tcsetattr(
                sys.stdin.fileno(), termios.TCSADRAIN, self.state
            )
            self.state = None

    def __get_escape_sequence(self) -> str | None:
        """Read and assemble an escape sequence from stdin.

        Returns:
            The matched escape sequence, or ``None`` if no valid sequence is
            recognized.
        """
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

    def __parse_keypress(self, char: str) -> KeyPress:
        """Convert a single input character into a key press object.

        Args:
            char: The character or escape sequence prefix read from stdin.

        Returns:
            A ``KeyPress`` representing the key or Unicode character.

        Raises:
            TerminalError: If no character is available to read.
        """
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

        key = KEY_SEQUENCES.get(sequence, None)
        if key is None:
            return KeyPress(key=Key.UNKNOWN)
        return KeyPress(key=key)

    def getch(self) -> KeyPress:
        """Read a single key press from standard input.

        Returns:
            The decoded key press.
        """
        try:
            char = sys.stdin.read(1)
            return self.__parse_keypress(char=char)
        except Exception:
            self.restore()
            raise

    def getch_nowait(self) -> KeyPress | None:
        """Read a key press without blocking if no input is available.

        Returns:
            The decoded key press, or ``None`` when no input is pending.
        """
        try:
            ready, _, _ = select.select([sys.stdin], [], [], 0)
            if ready:
                char = sys.stdin.read(1)
                return self.__parse_keypress(char=char)
            else:
                return None
        except Exception:
            self.restore()
            raise

    #  color management
    def __get_color_sequence(
        self,
        color: Color | tuple[int, int, int],
        foreground: bool,
    ) -> str:
        """Build an ANSI color sequence for a named or RGB color.

        Args:
            color: A color enum or an ``(R, G, B)`` tuple.
            foreground: Whether the color should be applied to foreground text.

        Returns:
            The ANSI escape sequence for the requested color.

        Raises:
            TypeError: If the color is not a supported enum or tuple.
            ValueError: If the RGB tuple does not contain three values or falls
                outside the valid range.
        """
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
        """Set the terminal foreground color.

        Args:
            color: A color enum or an ``(R, G, B)`` tuple.
        """
        sequence = self.__get_color_sequence(
            color=color, foreground=True
        )
        sys.stdout.write(sequence)

    def set_background_color(
        self,
        color: Color | tuple[int, int, int]
    ) -> None:
        """Set the terminal background color.

        Args:
            color: A color enum or an ``(R, G, B)`` tuple.
        """
        sequence = self.__get_color_sequence(
            color=color, foreground=False
        )
        sys.stdout.write(sequence)

    def set_color(
        self,
        foreground: Color | tuple[int, int, int] | None = None,
        background: Color | tuple[int, int, int] | None = None,
    ) -> None:
        """Set one or both terminal colors.

        Args:
            foreground: The foreground color to apply.
            background: The background color to apply.
        """
        if foreground is not None:
            self.set_foreground_color(color=foreground)
        if background is not None:
            self.set_background_color(color=background)

    def set_font_style(self, style: FontStyle) -> None:
        """Apply an ANSI font style.

        Args:
            style: The font style to enable.
        """
        sys.stdout.write(f"{CSI}{FONT_STYLES[style]}m")

    def reset_font_style(self, style: FontStyle) -> None:
        """Reset a specific ANSI font style.

        Args:
            style: The font style to reset.
        """
        sys.stdout.write(f"{CSI}{FONT_RESETS[style]}m")
