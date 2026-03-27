def error_exit():
    print("\033[1;31m!!--xxERRORxx--!!\033[0m")
    exit()


def key_missing():
    print("\033[1;31m!!--xxKEY_MISSINGxx--!!\033[0m")
    exit()


def key_checking(vals):
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "OUTPUT_FILE", "PERFECT"]
    for key in mandatory_keys:
        if key not in vals:
            key_missing()


def parse_conf():
    try:
        with open("config.txt") as file:
            vals = {}
            for line in file:
                line = line.strip()
                if line.startswith('#') or line == "":
                    continue
                try:
                    key, value = line.split('=', 1)
                except ValueError:
                    error_exit()
                key = key.upper().strip()
                value = value.strip()
                if key == "WIDTH" or key == "HEIGHT":
                    try:
                        new_val = int(value)
                    except ValueError:
                        error_exit()
                    vals[key] = new_val
                elif key == "ENTRY" or key == "EXIT":
                    i = 0
                    for _ in value.split(','):
                        i += 1
                    if i != 2:
                        error_exit()
                    val1, val2 = value.split(',')
                    try:
                        val1 = int(val1)
                        val2 = int(val2)
                    except ValueError:
                        error_exit()
                    new_val = (val1, val2)
                    vals[key] = new_val
                elif key == "PERFECT":
                    value = value.lower()
                    if value == "true":
                        new_val = True
                    elif value == "false":
                        new_val = False
                    else:
                        error_exit()
                    vals[key] = new_val
                else:
                    vals[key] = value
    except FileNotFoundError:
        error_exit()
    return vals


def validate_conf(vals):
    key_checking(vals)
    if vals["HEIGHT"] <= 0 or vals["WIDTH"] <= 0:
        error_exit()
    for x, y in [vals["ENTRY"], vals["EXIT"]]:
        if not ((0 <= x < vals["WIDTH"]) and (0 <= y < vals["HEIGHT"])):
            error_exit()
    if vals["ENTRY"] == vals["EXIT"]:
        error_exit()


def get_conf():
    vals = parse_conf()
    validate_conf(vals)
    return vals
vals = get_conf()
for key in vals:
    print(f"{key} = {vals[key]}")
