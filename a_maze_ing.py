import random
import copy
from pars import get_conf
from Enums import Cells


class MazeGenerator:
    def __init__(self) -> None:
        self.__height = 0
        self.__width = 0
        self.start = (0, 0)
        self.end = (0, 0)
        self.is_perfect = True
        self.__maze: list[list[str]] = []
        self.__path: list[type[int]] = []

    def update(self) -> None:
        values = get_conf()
        self.__height = values["HEIGHT"] * 2 + 1
        self.__width = values["WIDTH"] * 2 + 1
        sx, sy = values["ENTRY"]
        ex, ey = values["EXIT"]
        self.is_perfect = values["PERFECT"]
        self.start = (sx * 2 + 1, sy * 2 + 1)
        self.end = (ex * 2 + 1, ey * 2 + 1)

    def __range_42_pos(self) -> list[tuple]:
        cords: list[tuple] = [(0, 0),  (0, 2), (0, 4),
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
                    maze[y][x] = "  "
                x += 1
            y += 1
            x = 0
            while x in range(self.__width):
                maze[y][x] = Cells.Wall.value
                x += 1
            y += 1
        return maze

    def generate_maze(self) -> None:
        self.update()
        self.__maze = self.__make_first_maze()
        start_point = [self.start]
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
        if not self.is_perfect:
            self.not_perfect()
        self.path_finder()
        self.get_output()

    def get_output(self):
        binary: list[list[str]] = []
        i = 0
        y = 1
        with open(get_conf()["OUTPUT_FILE"], "w") as fd:
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
            x, y = get_conf()["ENTRY"]
            fd.write(f"{x},{y}\n")
            x, y = get_conf()["EXIT"]
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

    def not_perfect(self):
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

    def path_finder(self):
        start_paths = [[self.start]]
        while len(start_paths):
            paths = copy.deepcopy(start_paths)
            start_paths = []
            for path in paths:
                pos = path[len(path) - 1]
                if pos == self.end:
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

    def get_maze(self):
        return self.__maze

    def get_path(self):
        return self.__path
