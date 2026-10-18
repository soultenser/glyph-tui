
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

    @staticmethod
    def __position_validator(
        position: Position,
        directions: tuple[Position, Position, Position]
    ) -> None:
        if not isinstance(position, Position):
            raise TypeError(
                "position must be a Position."
            )
        if position not in directions:
            raise ValueError(
                "position is not allowed here."
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
    def font_style(self) -> frozenset[FontStyle]:
        return frozenset(self.__font_style)

    @font_style.setter
    def font_style(self, value: set[FontStyle]) -> None:
        if not isinstance(value, set):
            raise TypeError(
                "font_style must be a set of FontStyle values."
            )
        if any(not isinstance(style, FontStyle) for style in value):
            raise ValueError(
                "font_style must be a set of FontStyle values."
            )
        self.__font_style = value

    @property
    def padding(self) -> tuple[int, int, int, int]:
        return self.__padding

    @padding.setter
    def padding(self, value: tuple[int, int, int, int]) -> None:
        if not isinstance(value, tuple):
            raise TypeError(
                "padding must be a tuple of four integers."
            )
        if len(value) != 4:
            raise ValueError(
                "padding must contain exactly four values."
            )
        if any(type(nbr) is not int for nbr in value):
            raise TypeError(
                "padding values must be integers."
            )
        if any(nbr < 0 for nbr in value):
            raise ValueError(
                "padding values must be non-negative integers."
            )
        self.__padding = value

    @property
    def justify(self) -> Position:
        return self.__justify

    @justify.setter
    def justify(self, value: Position) -> None:
        self.__position_validator(
            position=value,
            directions=(Position.LEFT, Position.RIGHT, Position.CENTER)
        )
        self.__justify = value

    @property
    def align(self) -> Position:
        return self.__align

    @align.setter
    def align(self, value: Position) -> None:
        self.__position_validator(
            position=value,
            directions=(Position.TOP, Position.BOTTOM, Position.CENTER)
        )
        self.__align = value

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: object) -> None:
        self.__title = str(value)

    @property
    def justify_title(self) -> Position:
        return self.__justify_title

    @justify_title.setter
    def justify_title(self, value: Position) -> None:
        self.__position_validator(
            position=value,
            directions=(Position.LEFT, Position.RIGHT, Position.CENTER)
        )
        self.__justify_title = value

    @property
    def footer(self) -> str:
        return self.__footer

    @footer.setter
    def footer(self, value: object) -> None:
        self.__footer = str(value)

    @property
    def justify_footer(self) -> Position:
        return self.__justify_footer

    @justify_footer.setter
    def justify_footer(self, value: Position) -> None:
        self.__position_validator(
            position=value,
            directions=(Position.LEFT, Position.RIGHT, Position.CENTER)
        )
        self.__justify_footer = value


class CellStyle:
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
    def font_style(self) -> frozenset[FontStyle] | None:
        if self.__font_style is None:
            return None
        return frozenset(self.__font_style)

    @font_style.setter
    def font_style(self, value: set[FontStyle] | None) -> None:
        if value is not None and not isinstance(value, set):
            raise TypeError(
                "font_style must be a set of FontStyle values."
            )
        if value and any(not isinstance(style, FontStyle) for style in value):
            raise TypeError(
                "font_style must be a set of FontStyle values."
            )
        self.__font_style = value
