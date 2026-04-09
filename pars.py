from typing import Dict, List, Any
from Enums import color
import sys


def error_exit(msg: str = "Unexpected maze error") -> None:
    raise Exception(f"\033[1;31m!!--xxERRORxx--!! {msg}.\033[0m")


def key_missing(key: str) -> None:
    raise Exception("\033[1;31m!!--xxKEY_MISSINGxx--!! "
                    f"Missing mandatory key: {key}\033[0m")


def key_checking(vals: Dict[str, Any]) -> None:
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "OUTPUT_FILE", "PERFECT", "SEED"]
    for key in mandatory_keys:
        if key not in vals:
            key_missing(key)


def validate_output_file(path: str) -> None:
    if not path or not path.strip():
        error_exit("OUTPUT_FILE cannot be empty")
    path = path.strip()


def parse_conf() -> Dict[str, Any]:
    try:
        with open(sys.argv[1], "rb") as file:
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
    vals: Dict[str, Any] = {}
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
                vals[key] = None
            else:
                vals[key] = new_val
    return vals


def get_conf() -> Dict[str, Any]:
    if len(sys.argv) < 2:
        print("\033[1;31m!!--xxCONFIG_ERRORxx--!!'.\033[0m")
        print(f"{color.Red.value}\033[1;30mUSE: "
              "'python3 a_maze_int.py <config_file>'")
        sys.exit(1)
    vals = parse_conf()
    return vals
