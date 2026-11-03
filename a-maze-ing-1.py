import sys


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
        x, y = key.split(",")
        try:
            maze_config.set_entry((int(x), int(y)))
        except ValueError:
            sys.stderr.write(f"Invalid config key {key}\n\n")
            return
    if key == "EXIT":
        x, y = key.split(",")
        try:
            maze_config.set_exit((int(x), int(y)))
        except ValueError:
            sys.stderr.write(f"Invalid config key {key}\n\n")
            return
    if key == "OUTPUT_FILE":
        maze_config.set_output_file(value)
    if key == "PERFECT":
        if value == "True" or value == "true" or value == "TRUE":
            maze_config.set_perfect(True)
        else:
            maze_config.set_perfect(False)


def check_maze_config(maze_config: MazeConfigData) -> bool:
    if maze_config.get_width() is None:
        return False
    if maze_config.get_height() is None:
        return False
    if maze_config.get_entry() is None:
        return False
    if maze_config.get_exit() is None:
        return False
    if maze_config.get_output_file() is None:
        return False
    if maze_config.get_perfect() is None:
        return False
    return True

#TODO: ERROR HANDLING
def config_parser() -> MazeConfigData | None:
    data_set: set[str] = {"WIDTH", "HEIGHT", "ENRTY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    maze_config: MazeConfigData = MazeConfigData()
    with open("config.txt", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split("=")
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


def simple_maze_gen(maze_config: MazeConfigData) -> None:
    pass


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
