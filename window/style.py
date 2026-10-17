
import dataclasses as dc
import enum

from terminal import (
    Color,
    FontStyle,
)


t_color = tuple[int, int, int] | Color


class Position(enum.Enum):
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
        self.justify: Position = Position.LEFT
        self.align: Position = Position.TOP
        self.title: str = ""
        self.justify_title: Position = Position.LEFT
        self.footer: str = ""
        self.justify_footer: Position = Position.LEFT

    @staticmethod
    def __color_validator(color: t_color) -> None:
        if not isinstance(color, tuple) and not isinstance(color, Color):
            raise TypeError(
                "color must be a Color or an RGB tuple."
            )

        if isinstance(color, tuple):
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
    def border(self) -> t_color | None:
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
            raise ValueError("font_style must be a set of FontStyle values.")
        self.__font_style = value

    @property
    def padding(self) -> tuple[int, int, int, int]:
        return self.__padding

    @padding.setter
    def padding(self, value: tuple[int, int, int, int]) -> None:
        if not isinstance(value, tuple):
            raise ValueError("padding must be a tuple of four integers.")

        if len(value) != 4:
            raise ValueError("padding must contain exactly four values.")

        if any(type(nbr) is not int for nbr in value):
            raise TypeError("padding values must be integers.")

        if any(nbr < 0 for nbr in value):
            raise ValueError("padding values must be non-negative integers.")
        self.__padding = value


class StyleCell:
    def __init__(self) -> None:
        self.background: t_color | None = None
        self.foreground: t_color | None = None
        self.font_style: set[FontStyle] | None = None

    @staticmethod
    def __color_validator(color: t_color) -> None:
        if not isinstance(color, tuple) and not isinstance(color, Color):
            raise TypeError(
                "color must be a Color or an RGB tuple."
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
    def font_style(self, value: set[FontStyle] | None) -> None:
        if value and any(not isinstance(style, FontStyle) for style in value):
            raise ValueError("font_style must be a set of FontStyle values.")
        self.__font_style = value
