
import shutil
import sys
import typing

from .sequences import (
    CLEAR_LINE,
    CLEAR_SCREEN,
    CURSOR_HOME,
    CURSOR_HIDE,
    CURSOR_POSITION,
    CURSOR_SHOW,
)


class Terminal:

    def write(self, text: str) -> None:
        sys.stdout.write(text)

    def flush(self) -> None:
        sys.stdout.flush()

    @typing.overload
    def move_cursor(self, x: int, y: int) -> None:
        ...

    @typing.overload
    def move_cursor(self, position: tuple[int, int]) -> None:
        ...

    def move_cursor(
        self,
        x: int | tuple[int, int],
        y: int | None = None,
    ) -> None:

        if isinstance(x, tuple):
            if y is not None:
                raise TypeError(
                    "move_cursor() accepts either a position tuple (x, y) "
                    "or two separate coordinates (x, y), not both."
                )

            x, y = x
        elif y is None:
            raise TypeError(
                "move_cursor() missing required argument 'y'. "
                "Use move_cursor(x, y) or move_cursor(position)."
            )

        if type(x) is not int or type(y) is not int:
            raise TypeError("Coordinates must be integers.")

        if x < 0 or y < 0:
            raise ValueError("Coordinates must be non-negative integers.")

        cursor = CURSOR_POSITION.format(row=y + 1, column=x + 1)
        sys.stdout.write(cursor)

    def move_cursor_home(self) -> None:
        sys.stdout.write(CURSOR_HOME)

    def clear_screen(self) -> None:
        sys.stdout.write(CLEAR_SCREEN)

    def clear_line(self) -> None:
        sys.stdout.write(CLEAR_LINE)

    def set_cursor_visible(self, visible: bool = True) -> None:
        cursor = CURSOR_SHOW if visible else CURSOR_HIDE
        sys.stdout.write(cursor)

    def get_size(self) -> tuple[int, int]:
        size = shutil.get_terminal_size()
        return (size.columns, size.lines)
