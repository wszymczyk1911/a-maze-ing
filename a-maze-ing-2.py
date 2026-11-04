import sys
from dataclasses import dataclass


class ConfigError(Exception):
    def __init__(self, message: str = "Unknown Config Error") -> None:
        super().__init__(message)


@dataclass(frozen=True)
class MazeConfig:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool

    def __post_init__(self) -> None:
        if self.width < 2 or self.height < 2:
            raise ConfigError("width and height must be at least 2!")

def build_config(config_dict: dict[str, str]) -> MazeConfig:
    try:
        width = int(config_dict["WIDTH"])
        height = int(config_dict["HEIGHT"])
        entry = (int(config_dict["ENTRY"][0]), int(config_dict["ENTRY"][1]))
        exi_t = (int(config_dict["EXIT"][0]), int(config_dict["EXIT"][1]))
        output_file = config_dict["OUTPUT_FILE"]
        if config_dict["PERFECT"].lower() == "true":
            perfect = True
        elif config_dict["PERFECT"].lower() == "false":
            perfect = False
        else:
            raise ConfigError("Unknown perfect mode!")
    except (KeyError, ValueError) as e:
        raise ConfigError(f"[Config Error] Error building MazeConfig object: {e}")
    return MazeConfig(
        width, height, entry, exi_t, output_file, perfect
    )

def read_maze_config(config_file: str) -> dict[str, str]:
    required_keys: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    config_dict: dict[str, str] = {}
    try:
        with open(config_file, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("#") or line == "" or line == "\n":
                    continue
                try:
                    key, value = line.split("=")  # how does it work on 1=1=1 ?
                except ValueError:
                    raise ConfigError(f"Invalid Config Entry: {line}")
                if key not in required_keys:
                    raise ConfigError(f"Invalid Config Key: {key}")
                config_dict[key] = value
    except (OSError, UnicodeDecodeError) as e:
        raise ConfigError(f"[Config Error] Cannot read file {config_file}: {e}")
    config_keys = set(config_dict.keys())
    missing = required_keys - config_keys
    if missing:
        raise ConfigError(f"Missing Config Keys: {', '.join(sorted(missing))}")
    unknown = config_keys - required_keys
    if unknown:
        raise ConfigError(f"Unknown Config Keys: {', '.join(sorted(unknown))}")
    return config_dict


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 a-maze-ing-2.py <config_file>")
    config_file: str = sys.argv[1]
    config: MazeConfig = build_config(read_maze_config(config_file))


if __name__ == "__main__":
    main()
