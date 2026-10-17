
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
        self.border: t_color | None = None
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
    def border(self) -> bool:
        return self.__border

    @border.setter
    def border(self, value: t_color | None) -> None:
        if value is not None:
            self.__color_validator(color=value)
        self.__border = value

    @property
    def background(self) -> t_color | None:
        return self.__background

    @background.setter
    def background(self, value: t_color | None) -> None:
        if value is not None:
            self.__color_validator(color=value)
        self.__background = value

    @property
    def foreground(self) -> t_color | None:
        return self.__foreground

    @foreground.setter
    def foreground(self, value: t_color | None) -> None:
        if value is not None:
            self.__color_validator(color=value)
        self.__foreground = value

    @property
    def font_style(self) -> set[FontStyle]:
        return self.__font_style

    @font_style.setter
    def font_style(self, value: set[FontStyle]) -> None:
        if any(not isinstance(style, FontStyle) for style in value):
            raise ValueError()
        self.__font_style = value


@dc.dataclass
class StyleCell:
    background: t_color | None = None
    foreground: t_color | None = None
    font_style: set[FontStyle] | None = None
