from a_maze_ing import MazeGenerator
from Printer import Printer

if __name__ == "__main__":
    generator = MazeGenerator()
    Printer(generator).print_maze()
