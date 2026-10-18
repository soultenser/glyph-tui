
from .style import CellStyle


class Cell:
    def __init__(self) -> None:
        self.char: str = " "
        self.style: CellStyle = CellStyle()

    @property
    def char(self) -> str:
        return self.__char

    @char.setter
    def char(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                "char must be a string."
            )
        if len(value) != 1:
            raise ValueError(
                "char must contain exactly one character."
            )
        self.__char = value

    @property
    def style(self) -> CellStyle:
        return self.__style

    @style.setter
    def style(self, value: CellStyle) -> None:
        if not isinstance(value, CellStyle):
            raise TypeError(
                "style must be a CellStyle instance."
            )
        self.__style = value
