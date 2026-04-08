from subprocess import Popen
from Enums import Cells
try:
    import readchar
except ModuleNotFoundError:
    ...


class Player:
    def __init__(self, pos, time) -> None:
        self.pos = pos
        self.time = time
        self.music = True
        self.sfx = True

    def __check_path(self, path) -> None:
        if self.pos in path:
            Popen(["afplay", "songs/correct.wav"])
        else:
            Popen(["afplay", "songs/wrong.wav"])

    def playing(self, maze, path) -> bool:
        print("^: Move up")
        print(">: Move left")
        print("v: Moha Down")
        print("<: Move Right")
        print("M: Turn Off/On Music")
        print("N: Turn Off/On SFX")
        print("Q: Quit Play Mode")
        choice = readchar.readkey()
        x, y = self.pos
        match choice:
            case readchar.key.UP:
                if maze[y - 1][x] != Cells.Wall.value:
                    self.pos = (x, y - 2)
                    if self.sfx:
                        Popen(["afplay", "songs/walk.wav"])
                        self.__check_path(path)
                elif self.sfx:
                    Popen(["afplay", "songs/wall.wav"])
            case readchar.key.LEFT:
                if maze[y][x - 1] != Cells.Wall.value:
                    self.pos = (x - 2, y)
                    if self.sfx:
                        Popen(["afplay", "songs/walk.wav"])
                        self.__check_path(path)
                elif self.sfx:
                    Popen(["afplay", "songs/wall.wav"])
            case readchar.key.DOWN:
                if maze[y + 1][x] != Cells.Wall.value:
                    self.pos = (x, y + 2)
                    if self.sfx:
                        Popen(["afplay", "songs/walk.wav"])
                        self.__check_path(path)
                elif self.sfx:
                    Popen(["afplay", "songs/wall.wav"])
            case readchar.key.RIGHT:
                if maze[y][x + 1] != Cells.Wall.value:
                    self.pos = (x + 2, y)
                    if self.sfx:
                        Popen(["afplay", "songs/walk.wav"])
                        self.__check_path(path)
                elif self.sfx:
                    Popen(["afplay", "songs/wall.wav"])
            case "q":
                return True
            case "m":
                self.music = not self.music
            case "n":
                self.sfx = not self.sfx
            case _:
                return False
        return False
