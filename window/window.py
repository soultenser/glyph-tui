
from .style import Style


class Window:
    def __init__(
        self,
        x: int, y: int,
        width: int, height: int,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = Style()
        self.__children = []
        self.__parent = None

    @staticmethod
    def __validate_value(value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                "value must be an integer"
            )
        if isinstance(value, bool):
            raise TypeError(
                "value must not be a boolean"
            )
        if value < 0:
            raise ValueError(
                "value must be greater than or equal to 0"
            )

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int) -> None:
        self.__validate_value(value=value)
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int) -> None:
        self.__validate_value(value=value)
        self.__y = value

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, value: int) -> None:
        self.__validate_value(value=value)
        if value == 0:
            raise ValueError(
                "width must be greater than 0"
            )
        self.__width = value

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, value: int) -> None:
        self.__validate_value(value=value)
        if value == 0:
            raise ValueError(
                "height must be greater than 0"
            )
        self.__height = value

    @property
    def position(self) -> tuple[int, int]:
        return (self.__x, self.__y)

    @property
    def size(self) -> tuple[int, int]:
        return (self.__width, self.__height)

    @property
    def parent(self) -> "Window" | None:
        return self.__parent

    @parent.setter
    def parent(self, value: "Window" | None) -> None:
        if value is not None:
            if not isinstance(value, Window):
                raise TypeError(
                    "parent must be a Window instance or None"
                )
        self.__parent = value

    @property
    def children(self) -> "Window":
        return self.__children

    def add_child(self, child: "Window") -> None:
        pass
