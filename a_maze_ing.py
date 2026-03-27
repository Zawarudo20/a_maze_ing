import random
import time
import os
import pars

bg_green = "\033[42m"
bg_red = "\033[41m"
maze_bg = "\033[0m"


wall = "██"
not_visited = "xx"
visited = "  "




class MazeGenerator:
    def __init__(self) -> None:
        values = pars.get_conf()
        self.__height = values["HEIGHT"] * 2 + 1
        self.__width = values["WIDTH"] * 2 + 1
        sx, sy = values["ENTRY"]
        ex, ey = values["EXIT"]
        self.__start = (sx * 2 + 1, sy * 2 + 1)
        self.__end = (ex * 2 + 1, ey * 2 + 1)
        self.__maze: list[list[str]] = []
        self.generate_maze()

    def __make_first_maze(self) -> list[list[str]]:
        maze = [["xx" for _ in range(self.__width)]
                for _ in range(self.__height)]
        x = 0
        while x in range(self.__width):
            maze[0][x] = wall
            x += 1
        y = 1
        while y in range(self.__height):
            x = 0
            while x in range(self.__width):
                maze[y][x] = wall
                x += 1
                if (x, y) in self.__range_42_pos():
                    maze[y][x] = "  "
                x += 1
            y += 1
            x = 0
            while x in range(self.__width):
                maze[y][x] = wall
                x += 1
            y += 1
        return maze

    def generate_maze(self):
        self.__maze = self.__make_first_maze()
        random.seed(1337)
        start_point = [self.__start]
        while start_point:
            point = random.choice(start_point)
            x, y = point
            self.__maze[y][x] = visited
            directions = []
            if x + 2 < self.__width and self.__maze[y][x + 2] == not_visited:
                directions.append((y, x + 2, y, x + 1))
            if x - 2 > 0 and self.__maze[y][x - 2] == not_visited:
                directions.append((y, x - 2, y, x - 1))
            if y + 2 < self.__height and self.__maze[y + 2][x] == not_visited:
                directions.append((y + 2, x, y + 1, x))
            if y - 2 > 0 and self.__maze[y - 2][x] == not_visited:
                directions.append((y - 2, x, y - 1, x))
            if len(directions) == 0:
                start_point.remove((x, y))
                continue
            choice = random.choice(directions)
            self.__maze[choice[0]][choice[1]] = visited
            self.__maze[choice[2]][choice[3]] = "  "
            start_point.append((choice[1], choice[0]))
            time.sleep(0.01)
            os.system('clear')
            self.printing()


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

    def get_output(self):
        binary: list[list[str]] = []
        i = 0
        y = 1
        with open("maze.txt", "w") as fd:
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
                        if self.__maze[direction[1]][direction[0]] == wall:
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
            fd.write(f"{self.__start[0]},{self.__start[1]}\n")
            fd.write(f"{self.__end[0]},{self.__end[1]}\n")

    def get_maze(self) -> list[list[str]]:
        return self.__maze

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

    def printing(self):
        y = 0
        for arr in self.__maze:
            x = 0
            for char in arr:
                if self.__start == (x, y):
                    print(f"{bg_red}  \033[0m", end="")
                elif self.__end == (x, y):
                    print(f"{bg_green}  \033[0m", end="")
                elif (x, y) in self.__range_42_pos():
                    print(f"\033[100m{char}\033[0m", end="")
                else:
                    print(f"{maze_bg}{char}\033[0m", end="")
                x += 1
            print("")
            y += 1


def main():
    maze = MazeGenerator()
    maze.not_perfect()
    maze.get_output()
    os.system('clear')
    maze.printing()
    wait = True
    while wait:
        print("=== a-maze-ing ===")
        print("1. Re-generate a new maze")
        print("3. Rotate maze colors")
        print("4. quit")
        choice = input("Choice? (1-4): ")
        if choice == "1":
            os.system('clear')
            maze.__init__()
            maze.not_perfect()
            maze.get_output()
            os.system('clear')
            maze.printing()
        elif choice == "3":
            os.system('clear')
            maze.printing()
            print("1. white")
            print("2. yellow")
            print("3. blue")
            color = input("Chose your color : ")
            global maze_bg
            if color == "1":
                maze_bg = "\033[0m"
            elif color == "2":
                maze_bg = "\033[33m"
            elif color == "3":
                maze_bg = "\033[34m"
            else:
                os.system('clear')
                maze.printing()
                print(f"'{choice}' is not a valid input")
                continue
            os.system('clear')
            maze.printing()
        elif choice == "4":
            wait = False
        else:
            os.system('clear')
            maze.printing()
            print(f"'{choice}' \033[38;2;255;0;0mis not a valid input\033[0m")


main()
