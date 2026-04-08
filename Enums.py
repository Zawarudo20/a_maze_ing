from enum import Enum


class Cells(Enum):
    Wall = "██"
    Visited = "  "
    Not_Visited = "xx"


class color(Enum):
    Black = "\033[40m"
    Red = "\033[41m"
    Green = "\033[42m"
    Yellow = "\033[43m"
    Blue = "\033[44m"
    Purple = "\033[45m"
    Cyan = "\033[46m"
    White = "\033[47m"
    Grey = "\033[100m"
    Default = "\033[0m"
