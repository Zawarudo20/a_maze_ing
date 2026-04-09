import random
import copy
import os
from typing import Any
from enum import Enum


class Cells(Enum):
    Wall = "██"
    Visited = "  "
    Not_Visited = "xx"


class Maze_Error(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class MazeGenerator():
    def __init__(self) -> None:
        self.__height = 0
        self.__width = 0
        self.__start = (0, 0)
        self.__end = (0, 0)
        self.__seed = None
        self.__output = ""
        self.__is_perfect = True
        self.__maze: list[list[str]] = []
        self.__path: list[tuple[int, int]] = []

    @staticmethod
    def check_values(values: dict[str,
                                  Any]) -> None:
        keys = ["HEIGHT", "WIDTH",
                "EXIT", "ENTRY",
                "SEED", "OUTPUT_FILE",
                "PERFECT"]
        if not isinstance(values, dict):
            raise Maze_Error("!!--xxMAZE_ERRORxx--!!"
                             " MazeGenerator Need Dict Parameter")
        missing = []
        for key in keys:
            try:
                if values.get(key) is None and key != "SEED":
                    missing.append(key)
                elif key == "SEED" and values[key]:
                    ...
            except KeyError:
                missing.append(key)
        if len(missing):
            raise Maze_Error("!!--xxMAZE_ERRORxx--!!"
                             f"Messing keys : {missing}")
        for key in values:
            value = values[key]
            if key == "WIDTH" or key == "HEIGHT":
                if not isinstance(value, int):
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                                     f"{key} must be an integer, "
                                     f"got '{type(value)}'.")
                if value < 12:
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                                     f"{key} is less than 42 range "
                                     f"(must be >= 12, got {value}")
            elif key == "ENTRY" or key == "EXIT":
                if not isinstance(value, tuple):
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                                     f"{key} must be a tuple[int, int]"
                                     " got {type(value)}")
                if len(value) != 2:
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                                     f"{key} must contain 2 integers "
                                     f"got {len(value)}")
                if not isinstance(value[0], int) or not isinstance(value[1],
                                                                   int):
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                                     f"{key} coordinates must be integer got"
                                     f" [{type(value[0])},{type(value[1])}]")
            elif key == "PERFECT":
                if not isinstance(value, bool):
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                                     f"{key} must be a bool.")
            elif key == "OUTPUT_FILE":
                if not isinstance(value, str):
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! Output file"
                                     " must be a string.")
                if '\x00' in value:
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! contains"
                                     "invalid characters.")
                if os.path.exists(value):
                    if not os.path.isfile(value):
                        raise Maze_Error(f"OUTPUT_FILE '{value}' "
                                         "exists but is not a regular file")
                    if not os.access(value, os.W_OK):
                        raise Maze_Error("!!--xxPERMISSION_ERRORxx--!! "
                                         f"'{value}' is not writable.")
                if value == "":
                    raise Maze_Error("!!--xxPERMISSION_ERRORxx--!! "
                                     "Output file Can't be empty.")
            elif key == "SEED":
                if not isinstance(value, (int, str, float, type(None))):
                    raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                                     f"{key} type is not supported for"
                                     f"seed got {type(value)}.")
        if values["ENTRY"] == values["EXIT"]:
            raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                             "Entry and exit can't be equals'.")
        x, y = values["ENTRY"]
        if not 0 <= x < values["WIDTH"] or not 0 <= y < values["HEIGHT"]:
            raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                             "Entry is out of maze range'.")
        x, y = values["EXIT"]
        if not 0 <= x < values["WIDTH"] or not 0 <= y < values["HEIGHT"]:
            raise Maze_Error("!!--xxMAZE_ERRORxx--!! "
                             "Exit is out of maze range'.")

    def __range_42_pos(self) -> list[tuple[int, int]]:
        cords: list[tuple[int, int]] = [(0, 0),  (0, 2), (0, 4),
                                        (2, 4),
                                        (4, 4),  (4, 6),  (4, 8),
                                        (8, 0),  (8, 4),  (8, 6),  (8, 8),
                                        (10, 0),  (10, 4),  (10, 8),
                                        (12, 0),  (12, 2),  (12, 4),  (12, 8)]
        w = 6
        h = 4
        if (self.__width // 2) % 2 == 0:
            w = 7
        if (self.__height // 2) % 2 == 0:
            h = 5
        range_42 = [(x + (self.__width - 1) // 2 - w,
                    y + (self.__height - 1) // 2 - h)
                    for (x, y) in cords]
        return range_42

    def __make_first_maze(self) -> list[list[str]]:
        maze = [["xx" for _ in range(self.__width)]
                for _ in range(self.__height)]
        x = 0
        while x in range(self.__width):
            maze[0][x] = Cells.Wall.value
            x += 1
        y = 1
        while y in range(self.__height):
            x = 0
            while x in range(self.__width):
                maze[y][x] = Cells.Wall.value
                x += 1
                if (x, y) in self.__range_42_pos():
                    maze[y][x] = Cells.Visited.value
                x += 1
            y += 1
            x = 0
            while x in range(self.__width):
                maze[y][x] = Cells.Wall.value
                x += 1
            y += 1
        return maze

    def __reset(self) -> None:
        self.__height = 0
        self.__width = 0
        self.__start = (0, 0)
        self.__end = (0, 0)
        self.__seed = None
        self.__output = ""
        self.__is_perfect = True
        self.__maze = []
        self.__path = []

    def update(self, values: dict[str, Any]) -> Exception | None:
        try:
            self.check_values(values)
        except Maze_Error as err:
            return err
        self.__height = values["HEIGHT"] * 2 + 1
        self.__width = values["WIDTH"] * 2 + 1
        sx, sy = values["ENTRY"]
        ex, ey = values["EXIT"]
        self.__seed = values["SEED"]
        self.__output = values["OUTPUT_FILE"]
        self.__is_perfect = values["PERFECT"]
        self.__start = (sx * 2 + 1, sy * 2 + 1)
        self.__end = (ex * 2 + 1, ey * 2 + 1)
        if self.__start in self.__range_42_pos():
            self.__reset
            return Maze_Error("!!--xxMAZE_ERRORxx--!! "
                              "Start Point is in 42 Range")
        if self.__end in self.__range_42_pos():
            self.__reset
            return Maze_Error("!!--xxMAZE_ERRORxx--!! "
                              "End Point is in 42 Range")
        try:
            open(self.__output, "w")
        except Exception:
            return Maze_Error("!!--xxMAZE_ERRORxx--!! "
                              "Output can't be directory")
        return None

    def generate_maze(self) -> Exception | None:
        if self.__width == 0:
            return Maze_Error("!!--xxMAZE_ERRORxx--!! there is "
                              "no data for maze generator")
        random.seed(self.__seed)
        self.__maze = self.__make_first_maze()
        start_point = [self.__start]
        while start_point:
            point = random.choice(start_point)
            x, y = point
            self.__maze[y][x] = Cells.Visited.value
            directions = []
            if (x + 2 < self.__width and
               self.__maze[y][x + 2] == Cells.Not_Visited.value):
                directions.append((y, x + 2, y, x + 1))
            if x - 2 > 0 and self.__maze[y][x - 2] == Cells.Not_Visited.value:
                directions.append((y, x - 2, y, x - 1))
            if (y + 2 < self.__height
               and self.__maze[y + 2][x] == Cells.Not_Visited.value):
                directions.append((y + 2, x, y + 1, x))
            if y - 2 > 0 and self.__maze[y - 2][x] == Cells.Not_Visited.value:
                directions.append((y - 2, x, y - 1, x))
            if len(directions) == 0:
                start_point.remove((x, y))
                continue
            choice = random.choice(directions)
            self.__maze[choice[0]][choice[1]] = Cells.Visited.value
            self.__maze[choice[2]][choice[3]] = "  "
            start_point.append((choice[1], choice[0]))
        if not self.__is_perfect:
            self.not_perfect()
        self.path_finder()
        self.get_output()
        return None

    def get_output(self) -> None:
        binary: list[list[str]] = []
        i = 0
        y = 1
        with open(self.__output, "w") as fd:
            while y in range(self.__height):
                binary.append([])
                x = 1
                j = 0
                while x in range(self.__width):
                    directions = [(x - 1, y),
                                  (x, y + 1),
                                  (x + 1, y),
                                  (x, y - 1)]
                    binary[i].append("")
                    for direction in directions:
                        if (self.__maze[direction[1]][direction[0]]
                           == Cells.Wall.value):
                            binary[i][j] += "1"
                        else:
                            binary[i][j] += "0"
                    fd.write(format(int(binary[i][j], 2), "X"))
                    j += 1
                    x += 2
                fd.write("\n")
                y += 2
                i += 1
            fd.write("\n")
            x, y = self.__start
            x = (x - 1) // 2
            y = (y - 1) // 2
            fd.write(f"{x},{y}\n")
            x, y = self.__end
            x = (x - 1) // 2
            y = (y - 1) // 2
            fd.write(f"{x},{y}\n")
            i = 2
            while i in range(len(self.__path)):
                xa, ya = self.__path[i]
                xb, yb = self.__path[i - 2]
                if xa > xb:
                    fd.write("E")
                elif xb > xa:
                    fd.write("W")
                elif ya > yb:
                    fd.write("S")
                elif yb > ya:
                    fd.write("N")
                i += 2
            fd.write("\n")

    def not_perfect(self) -> None:
        range_42 = self.__range_42_pos()
        y = 1
        while y in range(self.__height):
            x = 1
            while x in range(self.__width):
                if (
                    random.random() < 0.1
                    and x not in range(range_42[0][0] - 1, range_42[0][0] + 14)
                    and y not in range(range_42[0][1] - 1, range_42[0][1] + 10)
                   ):
                    dirctions = [(x + 1, y),
                                 (x - 1, y),
                                 (x, y + 1),
                                 (x, y - 1)]
                    choice = random.choice(dirctions)
                    if (
                        choice[0] != 0 and choice[0] != self.__width - 1
                        and choice[1] != 0 and choice[1] != self.__height - 1
                       ):
                        self.__maze[choice[1]][choice[0]] = "  "
                x += 2
            y += 2

    def path_finder(self) -> None:
        start_paths = [[self.__start]]
        while True:
            paths = start_paths
            start_paths = []
            for path in paths:
                pos = path[len(path) - 1]
                if pos == self.__end:
                    self.__path = path
                    for i in range(len(self.__maze)):
                        for j in range(len(self.__maze[i])):
                            if (self.__maze[i][j] == "XX"
                               or self.__maze[i][j] == "OO"):
                                self.__maze[i][j] = "  "
                    return
                x, y = pos
                directions = [(x + 1, y),
                              (x - 1, y),
                              (x, y + 1),
                              (x, y - 1)]
                self.__maze[y][x] = "XX"
                for direction in directions:
                    dx, dy = direction
                    if self.__maze[dy][dx] == "  ":
                        self.__maze[dy][dx] = "OO"
                        new_path = copy.deepcopy(path)
                        new_path.append((dx, dy))
                        start_paths.append(new_path)

    def get_data(self, name: str) -> Any:
        if not isinstance(name, str):
            return "parameter have to be string"
        name = name.lower()
        match name:
            case "maze":
                return self.__maze
            case "path":
                return self.__path
            case "height":
                return self.__height
            case "width":
                return self.__width
            case "start":
                return self.__start
            case "end":
                return self.__end
            case "seed":
                return self.__end
            case "output":
                return self.__output
            case "perfect":
                return self.__is_perfect
            case _:
                return f"{name} is invalid option"
