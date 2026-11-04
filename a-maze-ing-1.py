import sys
import random

DIRECTIONS = [
    (0, -1, "N"),
    (0, 1, "S"),
    (1, 0, "E"),
    (-1, 0, "W")
]

OPPOSITE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E"
}


# TODO: errors to handle:
# -> string.split() can fail
# -> width and height should be positive
# -> entry and exit should be inside the maze
class MazeConfigData:
    def __init__(self) -> None:
        self._width = None
        self._height = None
        self._entry = None
        self._exit = None
        self._output_file = None
        self._perfect = None

    def set_width(self, width: int) -> None:
        self._width = width

    def get_width(self) -> int | None:
        return self._width

    def set_height(self, height: int) -> None:
        self._height = height

    def get_height(self) -> int | None:
        return self._height

    def set_entry(self, entry: tuple[int, int]) -> None:
        self._entry = entry

    def get_entry(self) -> tuple[int, int] | None:
        return self._entry

    def set_exit(self, exi_t: tuple[int, int]) -> None:
        self._exit = exi_t

    def get_exit(self) -> tuple[int, int] | None:
        return self._exit

    def set_output_file(self, output_file: str) -> None:
        self._output_file = output_file

    def get_output_file(self) -> str | None:
        return self._output_file

    def set_perfect(self, perfect: bool) -> None:
        self._perfect = perfect

    def get_perfect(self) -> bool | None:
        return self._perfect


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls: dict[str, bool] = {
            "N": True,
            "S": True,
            "E": True,
            "W": True
        }
        self.visited = False


def config_helper(maze_config: MazeConfigData, key: str, value: str) -> None:
    if key == "WIDTH":
        try:
            maze_config.set_width(int(value))
        except ValueError:
            sys.stderr.write(f"Invalid config key {key}\n\n")
            return
    if key == "HEIGHT":
        try:
            maze_config.set_height(int(value))
        except ValueError:
            sys.stderr.write(f"Invalid config key {key}\n\n")
            return
    if key == "ENTRY":
        x, y = value.split(",")
        # print(f"x: {x}, y: {y}")
        try:
            maze_config.set_entry((int(x), int(y)))
        except ValueError:
            sys.stderr.write(f"Invalid config key {key}\n\n")
            return
    if key == "EXIT":
        x, y = value.split(",")
        try:
            maze_config.set_exit((int(x), int(y)))
        except ValueError:
            sys.stderr.write(f"Invalid config key {key}\n\n")
            return
    if key == "OUTPUT_FILE":
        maze_config.set_output_file(value)
    if key == "PERFECT":
        if value.lower() == "true":
            maze_config.set_perfect(True)
        elif value.lower() == "false":
            maze_config.set_perfect(False)
        else:
            sys.stderr.write(f"Value for key [perfect] should be either True or False\n\n")


def check_maze_config(maze_config: MazeConfigData) -> bool:
    if maze_config.get_width() is None:
        # print(f"width: {maze_config.get_width()}")
        return False
    if maze_config.get_height() is None:
        # print(f"height: {maze_config.get_height()}")
        return False
    if maze_config.get_entry() is None:
        # print(f"entry: {maze_config.get_entry()}")
        return False
    if maze_config.get_exit() is None:
        # print(f"exit: {maze_config.get_exit()}")
        return False
    if maze_config.get_output_file() is None:
        # print(f"output_file: {maze_config.get_output_file()}")
        return False
    if maze_config.get_perfect() is None:
        # print(f"perfect: {maze_config.get_perfect()}")
        return False
    return True


# TODO: ERROR HANDLING
def config_parser() -> MazeConfigData | None:
    data_set: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    maze_config: MazeConfigData = MazeConfigData()
    with open("config.txt", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split("=")
            # print(f"key = {key}")
            # print(f"value = {value}")
            if key not in data_set:
                sys.stderr.write(f"Invalid config key {key}\n\n")
                continue  # / sys.exit(1) ??????
            config_helper(maze_config, key, value)  # -> it can be in a try/except block and config_helper can raise
            # errors on its own excepts instead of writing error there
    check_res = check_maze_config(maze_config)
    if not check_res:
        sys.stderr.write(f"Invalid config file! Mandatory: WIDTH, HEIGHT, ENRTY, EXIT, OUTPUT_FILE, PERFECT\n\n")
        return None
    return maze_config


def print_maze(maze_grid: list[list[Cell]]) -> None:
    height = len(maze_grid)
    width = len(maze_grid[0])

    for y in range(height):
        top = ""
        middle = ""

        for x in range(width):
            cell = maze_grid[y][x]

            top += "+" + ("---" if cell.walls["N"] else "   ")
            middle += ("|" if cell.walls["W"] else " ") + "   "

        top += "+"
        middle += "|"

        print(top)
        print(middle)

    print("+" + "---+" * width)


def get_unvisited_neighbors(maze_grid: list[list[Cell]], cell: Cell) \
        -> list[tuple[Cell, str]]:
    neighbors: list[tuple[Cell, str]] = []
    x, y = cell.x, cell.y
    height = len(maze_grid)
    width = len(maze_grid[0])
    for horizontal, vertical, direction in DIRECTIONS:
        new_x = x + horizontal
        new_y = y + vertical
        if 0 <= new_x < width and 0 <= new_y < height:
            neighbor = maze_grid[new_y][new_x]
            if not neighbor.visited:
                neighbors.append((neighbor, direction))
    return neighbors


def remove_walls(current: Cell, neighbor: Cell, direction: str) -> None:
    current.walls[direction] = False
    neighbor.walls[OPPOSITE[direction]] = False


def recursive_backtracking(maze_grid: list[list[Cell]], current: Cell) -> None:
    current.visited = True
    while True:
        neighbors = get_unvisited_neighbors(maze_grid, current)
        if not neighbors:
            return
        neighbor, direction = random.choice(neighbors)
        remove_walls(current, neighbor, direction)
        recursive_backtracking(maze_grid, neighbor)


def simple_maze_gen(maze_config: MazeConfigData) -> None:
    width = maze_config.get_width()
    height = maze_config.get_height()
    if width is None or height is None:
        return
    # maze_grid = [[(x, y) for x in range(width)] for y in range(height)]           -> simple grid: a list of lists
    # for row in maze_grid:
    #     print(row)
    #                                                                               -> using Cells class:
    maze_grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
    print_maze(maze_grid)
    entry = maze_config.get_entry()
    if entry is None:
        sys.exit(1)
    x, y = entry
    recursive_backtracking(maze_grid, maze_grid[x][y])
    print_maze(maze_grid)


def main() -> None:
    print("A-MAZE-ING VERSION 1.0 <3")
    print("\nReading from config file .....")
    maze_config: MazeConfigData | None = config_parser()
    if maze_config is None:
        sys.stderr.write(f"Something went wrong! :( \n")
        sys.exit(1)
    print("Config file [OK]!")
    print("Let's generate maze! <3")
    simple_maze_gen(maze_config)


if __name__ == "__main__":
    main()
