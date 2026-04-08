from a_maze_ing import MazeGenerator
from time import sleep
from os import system
from subprocess import Popen
from Enums import color, Cells
try:
    from Player import Player
except ModuleNotFoundError:
    system("clear")
    print(f"{color.Red.value}Player.py File is missing "
          f"you Can't Play game mode{color.Default.value}")
    sleep(3)


class Printer:
    def __init__(self, generator) -> None:
        self.walls = color.White.value
        self.cell = color.Black.value
        self.logo = color.Grey.value
        self.path = color.Blue.value
        self.start = color.Red.value
        self.end = color.Green.value
        self.player = None
        self.print_path = False
        self.is_playing = False
        self.generator: MazeGenerator = generator

    @staticmethod
    def __error():
        system("clear")
        print(f"{color.Red.value}Invalid Input{color.Default.value}")
        sleep(1)

    def __parerr(self, err):
        system("clear")
        print(f"{color.Red.value}{err}{color.Default.value}")
        print("1. Try Again")
        print("2. Quit")
        choice = int(input("Choice? (1 - 2):"))
        match choice:
            case 1:
                return 1
            case 2:
                return 0
            case _:
                self.__error()

    def print_maze(self):
        if not isinstance(self.generator, MazeGenerator):
            print(f"{color.Red.value}There is no"
                  f" maze generator{color.Default.value}")
        while True:
            msg = self.generator.generate_maze()
            if msg:
                if self.__parerr(msg):
                    continue
                return
            break
        maze = self.generator.get_maze()
        height = (len(maze) - 1) / 2
        width = (len(maze[0]) - 1) / 2
        try:
            self.player = Player(self.generator.start, height * width * 0.1)
        except NameError:
            self.player = None
        while True:
            self.__printing()
            try:
                self.__options()
                return
            except Exception:
                self.__error()

    @staticmethod
    def __is_blocked(maze, pos):
        x, y = pos
        if (maze[y][x] == Cells.Visited.value
           and maze[y][x + 1] == Cells.Wall.value
           and maze[y][x - 1] == Cells.Wall.value
           and maze[y + 1][x] == Cells.Wall.value
           and maze[y - 1][x] == Cells.Wall.value):
            return True
        return False

    def __printing(self):
        system("clear")
        maze = self.generator.get_maze()
        path = self.generator.get_path()
        start = self.generator.start
        end = self.generator.end
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if self.__is_blocked(maze, (j, i)):
                    print(self.logo, end="")
                elif (j, i) == start:
                    print(self.start, end="")
                elif (j, i) == end:
                    print(self.end, end="")
                elif (j, i) in path and self.print_path:
                    print(self.path, end="")
                elif maze[i][j] == "  ":
                    print(self.cell, end="")
                elif maze[i][j] == Cells.Wall.value:
                    print(self.walls, end="")
                if not self.is_playing or (j, i) != self.player.pos:
                    print("  ", end="")
                elif (j, i) == self.player.pos:
                    print("🕺", end="")
            print("\033[0m")

    def __options(self):
        while True:
            print("=== A_Maze_ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze Colors")
            print("4. PlayGame")
            print("5. Quit")
            option = int(input("Choice? (1 - 5): "))
            match option:
                case 1:
                    while True:
                        msg = self.generator.generate_maze()
                        if msg:
                            if self.__parerr(msg):
                                continue
                            return
                        break
                case 2:
                    self.print_path = not self.print_path
                case 3:
                    system("clear")
                    print("1. Change Walls Color")
                    print("2. Change Cells Color")
                    print("3. Change Start Cell Color")
                    print("4. Change End Cell Color")
                    print("5. Change Path Color")
                    print("6. Change 42 Color")
                    choice = int(input("Choice? (1 - 6): "))
                    if choice < 1 or choice > 6:
                        self.__error()
                        self.__printing()
                        continue
                    system("clear")
                    print("1. Black")
                    print("2. Red")
                    print("3. Green")
                    print("4. Yellow")
                    print("5. Blue")
                    print("6. Purple")
                    print("7. Cyan")
                    print("8. White")
                    print("9. Grey")
                    num = int(input("Choice? (1 - 9): ")) - 1
                    colors = [color.Black, color.Red, color.Green,
                              color.Yellow, color.Blue, color.Purple,
                              color.Cyan, color.White, color.Grey]
                    match choice:
                        case 1:
                            self.walls = colors[num].value
                        case 2:
                            self.cell = colors[num].value
                        case 3:
                            self.start = colors[num].value
                        case 4:
                            self.end = colors[num].value
                        case 5:
                            self.path = colors[num].value
                        case 6:
                            self.logo = colors[num].value
                case 4:
                    if not self.player:
                        system("clear")
                        print(f"{color.Red.value}Player.py File is missing you"
                              f" Can't Play game mode{color.Default.value}")
                        sleep(3)
                    else:
                        try:
                            self.player.pos = self.generator.start
                            self.is_playing = True
                            tmp = self.print_path
                            self.print_path = False
                            proc = Popen(["afplay", "songs/Song.wav"])
                            while self.player.pos != self.generator.end:
                                if not proc.poll() and not self.player.music:
                                    proc.terminate()
                                elif proc.poll() and self.player.music:
                                    proc = Popen(["afplay", "songs/Song.wav"])
                                self.__printing()
                                if self.player.playing(
                                     self.generator.get_maze(),
                                     self.generator.get_path()):
                                    break
                            proc.terminate()
                            self.print_path = tmp
                            self.is_playing = False
                            self.player.pos = self.generator.start
                        except NameError:
                            self.print_path = tmp
                            proc.terminate()
                            system("clear")
                            print(f"{color.Red.value}Please Install ReadChar"
                                  f" to play the game{color.Default.value}")
                            sleep(2)
                case 5:
                    return
                case _:
                    self.__error()
            self.__printing()
