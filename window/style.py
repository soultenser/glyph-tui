
import dataclasses as dc
import enum

from terminal import (
    Color,
    FontStyle,
)


t_color = tuple[int, int, int] | Color


class Alignment(enum.Enum):
    LEFT = enum.auto()
    CENTER = enum.auto()
    RIGHT = enum.auto()
    TOP = enum.auto()
    BOTTOM = enum.auto()


class Style:
    def __init__(self) -> None:
        self.border: bool = False
        self.border_color: t_color = Color.WHITE
        self.background: t_color | None = None
        self.foreground: t_color | None = None
        self.font_style: set[FontStyle] = set()
        self.padding: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.justify: Alignment = Alignment.LEFT
        self.align: Alignment = Alignment.TOP
        self.title: str = ""
        self.justify_title: Alignment = Alignment.LEFT
        self.footer: str = ""
        self.justify_footer: Alignment = Alignment.LEFT

    @property
    def border(self) -> bool:
        return bool(self.__border)

    @border.setter
    def border(self, value: bool) -> None:
        if value not in (True, False, 1, 0):
            raise ValueError(
                "border must be a boolean or an integer equal to 0 or 1"
            )
        self.__border = value

    def __color_validator(color: t_color) -> None:
        if not isinstance(color, tuple) and not isinstance(color, Color):
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

    @property
    def border_color(self) -> t_color:
        return self.__border_color

    @border_color.setter
    def border_color(self, value: t_color) -> None:
        self.__color_validator(color=value)
        self.__border_color = value


@dc.dataclass
class StyleCell:
    background: t_color | None = None
    foreground: t_color | None = None
    font_style: set[FontStyle] | None = None
