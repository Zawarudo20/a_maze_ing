from typing import Dict, List, TypedDict, Tuple, cast
import os


class Config(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int


def error_exit(msg: str = "Unexpected maze error") -> None:
    raise Exception(f"\033[1;31m!!--xxERRORxx--!! {msg}.\033[0m")


def key_missing(key: str) -> None:
    raise Exception("\033[1;31m!!--xxKEY_MISSINGxx--!! "
                    f"Missing mandatory key: {key}\033[0m")


def key_checking(vals: Config) -> None:
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "OUTPUT_FILE", "PERFECT", "SEED"]
    for key in mandatory_keys:
        if key not in vals:
            key_missing(key)


def validate_output_file(path: str) -> None:
    if not path or not path.strip():
        error_exit("OUTPUT_FILE cannot be empty")
    path = path.strip()
    if '\x00' in path:
        error_exit("OUTPUT_FILE contains invalid characters")
    # _, ext = os.path.splitext(path)
    # if ext and ext != '.txt':
    #     raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
    #                      f"INVALID OUTPUT_FILE TYPE, GOT '{ext}' "
    #                      "INSTEAD OF '.txt'.\033[0m")
    if os.path.exists(path):
        if not os.path.isfile(path):
            error_exit(f"OUTPUT_FILE '{path}' "
                       "exists but is not a regular file")
        if not os.access(path, os.W_OK):
            raise PermissionError("\033[1;31m!!--xxPERMISSION_ERRORxx--!! "
                                  f"'{path}' is not writable.\033[0m")


def parse_conf() -> Config:
    try:
        with open("config.txt", "rb") as file:
            raw_bytes = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("\033[1;31m!!--xxFILE_NOT_FOUND_ERRORxx--!! "
                                "'config.txt' not found.\033[0m")
    except PermissionError:
        raise PermissionError("\033[1;31m!!--xxPERMISSION_ERRORxx--!! "
                              "'config.txt' is not readable.\033[0m")
    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise Exception("\033[1;31m!!--xxUNICODE_DECODE_ERRORxx--!! "
                        "'config.txt' contains binary or "
                        "non UTF-8 data.\033[0m")
    vals: Dict[str, object] = {}
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "OUTPUT_FILE", "PERFECT", "SEED"]
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('#') or line == "":
            continue
        try:
            key, value = line.split('=', 1)
        except ValueError:
            continue
        key = key.upper().strip()
        value = value.strip()
        if key not in mandatory_keys:
            continue
        if key == "WIDTH" or key == "HEIGHT":
            try:
                new_val = int(value)
            except ValueError:
                raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
                                 f"{key} must be an integer, "
                                 f"got '{value}'.\033[0m")
            if new_val < 12:
                raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
                                 f"{key} is out of 42 range (must be >= 12, "
                                 f"got {new_val}).\033[0m")
            vals[key] = new_val
        elif key == "ENTRY" or key == "EXIT":
            parts: List[str] = value.split(',')
            if len(parts) != 2:
                raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
                                 f"{key} must be in format X,Y\033[0m")
            try:
                val1 = int(parts[0])
                val2 = int(parts[1])
            except ValueError:
                raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
                                 f"{key} coordinates must be integers.\033[0m")
            vals[key] = (val1, val2)
        elif key == "PERFECT":
            value = value.lower()
            if value.lower() == "true":
                new_val = True
            elif value.lower() == "false":
                new_val = False
            else:
                raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
                                 f"{key} must be True or False, "
                                 f"got '{value}'.\033[0m")
            vals[key] = new_val
        elif key == "OUTPUT_FILE":
            validate_output_file(value)
            vals[key] = value.strip()
        elif key == "SEED":
            if value == '' or value.lower() == "none":
                vals[key] = -1
            else:
                try:
                    new_val = int(value)
                except ValueError:
                    raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
                                     f"{key} must be an integer, "
                                     f"got '{value}'.\033[0m")
                if new_val < 0:
                    raise ValueError("\033[1;31m!!--xxVALUE_ERRORxx--!! "
                                     f"{key} must be positive.\033[0m")
                else:
                    vals[key] = new_val
    return cast(Config, vals)


def validate_conf(vals: Config) -> None:
    key_checking(vals)
    if vals["HEIGHT"] <= 0 or vals["WIDTH"] <= 0:
        error_exit("WIDTH & HEIGHT must be positive.")
    for x, y in [vals["ENTRY"], vals["EXIT"]]:
        if not ((0 <= x < vals["WIDTH"]) and (0 <= y < vals["HEIGHT"])):
            error_exit("ENTRY & EXIT are outside maze bounds.")
    if vals["ENTRY"] == vals["EXIT"]:
        error_exit("ENTRY & EXIT must be different")


def get_conf() -> Config:
    vals = parse_conf()
    validate_conf(vals)
    return vals
