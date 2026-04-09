from subprocess import Popen
from Enums import Cells, color
from os import system
from time import sleep
from random import random, choice
try:
    import readchar
except ModuleNotFoundError:
    ...


class Creature:
    def __init__(self, name: str, health: int, DMG: int, DEF: int) -> None:
        self.name = name
        self.ascii_art: list[str] = []
        self.health = health
        self.dmg = DMG
        self.shield = DEF
        self.isguarded = False
        self.isalive = True
        self.pos = (0, 0)
        self.ascii()

    def ascii(self) -> None:
        match self.name:
            case "bat":
                self.ascii_art = [" /\\                 /\\",
                                  "/ \\'._   (\\_/)   _.'/ \\",
                                  "|.''._'--(o.o)--'_.''.|",
                                  "\\_ / `;=/ \" \\=;` \\ _/",
                                  "  `\\__| \\___/ |__/`",
                                  "        \\(_|_)/ "]
            case "dog":
                self.ascii_art = [" / \\__"
                                  "(    @\\___",
                                  " /         O",
                                  "/   (_____/",
                                  "/_____/   U"]
            case "snake":
                self.ascii_art = ["   /^\\/^\\",
                                  "_|  O O|",
                                  "\\/     /~",
                                  "\\____|",
                                  "  /  /",
                                  " /  /",
                                  "/  /"]
            case "67":
                self.ascii_art = ["66666   7777777",
                                  "6     6      7",
                                  "6           7",
                                  "666666     7",
                                  "6     6   7",
                                  "6     6   7",
                                  " 66666    7"]

    def attack(self, enemy: 'Creature') -> None:
        if enemy.isguarded:
            atk = self.dmg - enemy.shield
            if atk > 0:
                enemy.health -= atk
            enemy.isguarded = False
        else:
            enemy.health -= self.dmg


class Game:
    def __init__(self) -> None:
        self.music = True
        self.sfx = True
        self.player: Creature = Creature("Player", 50, 3, 2)
        self.enemys: list[Creature] = []

    def __check_path(self, path: list[tuple[int, int]]) -> None:
        if self.player.pos in path:
            Popen(["afplay", "songs/correct.wav"])
        else:
            Popen(["afplay", "songs/wrong.mp3"])

    def set_enemys(self, maze: list[list[str]],
                   start: tuple[int, int],
                   end: tuple[int, int]) -> None:
        names = ["dog", "bat", "snake", "67"]
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if (maze[i][j] == "  " and (j, i) != end
                   and (j, i) != start and random() < 0.01):
                    name = choice(names)
                    enemy = Creature(name, 10, 4, 0)
                    enemy.pos = (j, i)
                    self.enemys.append(enemy)

    def battle(self, enemy: Creature, proc: Popen[bytes]) -> bool:
        proc.terminate()
        if self.music:
            proc2 = Popen(["afplay", "songs/battle.mp3"])
        while enemy.health > 0 and self.player.health > 0:
            system("clear")
            print("\n\n\n")
            for arr in enemy.ascii_art:
                print(f"\t\t\t\t{arr}")
            print(f"Player HP = {self.player.health}")
            print(f"{enemy.name} HP = {enemy.health}")
            print("-" * 70)
            print("1.Fight\t\t\t2.Guard\t\t\t3.Run")
            choice = readchar.readkey()
            match choice:
                case "1":
                    self.player.attack(enemy)
                case "2":
                    self.player.isguarded = True
                case "3":
                    if self.music:
                        proc2.terminate()
                    return False
            enemy.attack(self.player)
        if self.music:
            proc2.terminate()
        return True

    def check_enemy(self, enemys: list[Creature], pos1: tuple[int, int],
                    pos2: tuple[int, int]) -> Creature | None:
        for enemy in enemys:
            if pos1 == enemy.pos or pos2 == enemy.pos:
                return enemy
        return None

    def playing(self, maze: list[list[str]],
                path: list[tuple[int, int]],
                start: tuple[int, int],
                end: tuple[int, int]) -> None:
        self.player = Creature("Player", 50, 3, 2)
        self.player.pos = start
        self.set_enemys(maze, start, end)
        printer = Game_printer()
        proc = Popen(["afplay", "songs/Song.wav"])
        while (True):
            printer.printing(maze, start, end, self)
            print("--------------------------------------------")
            print("^: Move up")
            print(">: Move left")
            print("v: Moha Down")
            print("<: Move Right")
            print("M: Turn Off/On Music")
            print("N: Turn Off/On SFX")
            print("Q: Quit Play Mode")
            choice = readchar.readkey()
            x, y = self.player.pos
            match choice:
                case readchar.key.UP:
                    if maze[y - 1][x] != Cells.Wall.value:
                        enemy = self.check_enemy(self.enemys,
                                                 (x, y - 2),
                                                 (x, y - 1))
                        if enemy:
                            result = self.battle(enemy, proc)
                            if result:
                                self.player.pos = (x, y - 2)
                                self.enemys.remove(enemy)
                        else:
                            self.player.pos = (x, y - 2)
                        if self.sfx:
                            Popen(["afplay", "songs/walk.wav"])
                            self.__check_path(path)
                    elif self.sfx:
                        Popen(["afplay", "songs/wall.wav"])
                case readchar.key.LEFT:
                    if maze[y][x - 1] != Cells.Wall.value:
                        enemy = self.check_enemy(self.enemys,
                                                 (x - 2, y),
                                                 (x - 1, y))
                        if enemy:
                            result = self.battle(enemy, proc)
                            if result:
                                self.player.pos = (x - 2, y)
                                self.enemys.remove(enemy)
                        else:
                            self.player.pos = (x - 2, y)
                            if self.sfx:
                                Popen(["afplay", "songs/walk.wav"])
                                self.__check_path(path)
                    elif self.sfx:
                        Popen(["afplay", "songs/wall.wav"])
                case readchar.key.DOWN:
                    if maze[y + 1][x] != Cells.Wall.value:
                        enemy = self.check_enemy(self.enemys,
                                                 (x, y + 2),
                                                 (x, y + 1))
                        if enemy:
                            result = self.battle(enemy, proc)
                            if result:
                                self.player.pos = (x, y + 2)
                                self.enemys.remove(enemy)
                        else:
                            self.player.pos = (x, y + 2)
                            if self.sfx:
                                Popen(["afplay", "songs/walk.wav"])
                                self.__check_path(path)
                    elif self.sfx:
                        Popen(["afplay", "songs/wall.wav"])
                case readchar.key.RIGHT:
                    if maze[y][x + 1] != Cells.Wall.value:
                        enemy = self.check_enemy(self.enemys,
                                                 (x + 2, y),
                                                 (x + 1, y))
                        if enemy:
                            result = self.battle(enemy, proc)
                            if result:
                                self.player.pos = (x + 2, y)
                                self.enemys.remove(enemy)
                        else:
                            self.player.pos = (x + 2, y)
                            if self.sfx:
                                Popen(["afplay", "songs/walk.wav"])
                                self.__check_path(path)
                    elif self.sfx:
                        Popen(["afplay", "songs/wall.wav"])
                case "q":
                    proc.terminate()
                    return
                case "m":
                    self.music = not self.music
                case "n":
                    self.sfx = not self.sfx
                case _:
                    continue
            if self.player.health <= 0:
                system("clear")
                print("\t\t\t\tYOU DIED")
                proc.terminate()
                sleep(3)
                return
            if not self.music and not proc.poll():
                proc.terminate()
            elif self.music and proc.poll():
                proc = Popen(["afplay", "songs/Song.wav"])
            if self.player.pos == end:
                print("\t\t\tYOU WIN")
                proc.terminate()
                sleep(3)
                return


class Game_printer:
    def __init__(self) -> None:
        self.walls = color.White.value
        self.cell = color.Black.value
        self.logo = color.Grey.value
        self.start = color.Red.value
        self.end = color.Green.value
        self.game: Game | None = None

    @staticmethod
    def __is_blocked(maze: list[list[str]], pos: tuple[int, int]) -> bool:
        x, y = pos
        if (maze[y][x] == Cells.Visited.value
           and maze[y][x + 1] == Cells.Wall.value
           and maze[y][x - 1] == Cells.Wall.value
           and maze[y + 1][x] == Cells.Wall.value
           and maze[y - 1][x] == Cells.Wall.value):
            return True
        return False

    def printing(self, maze: list[list[str]], start: tuple[int, int],
                 end: tuple[int, int], game: Game) -> None:
        system("clear")
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if self.__is_blocked(maze, (j, i)):
                    print(self.logo, end="")
                elif (j, i) == start:
                    print(self.start, end="")
                elif (j, i) == end:
                    print(self.end, end="")
                elif maze[i][j] == "  ":
                    print(self.cell, end="")
                elif maze[i][j] == Cells.Wall.value:
                    print(self.walls, end="")
                if (j, i) == game.player.pos:
                    print("🕺", end="")
                elif (any((j, i) == enemy.pos for enemy in game.enemys)
                      and not self.__is_blocked(maze, (j, i))):
                    print("😈", end="")
                else:
                    print("  ", end="")
            print("\033[0m")
