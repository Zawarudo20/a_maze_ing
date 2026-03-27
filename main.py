maze = [
    [6,4,4,4,12],
    [2,0,0,0,8],
    [2,0,15,2,8],
    [2,0,0,0,8],
    [3,1,1,1,9],
]

for arr in maze:
    for n in arr:
        if (n >= 4 and n <= 7) or (n >= 12 and n <= 15):
            print("██", end="")
        else:
            print("  ", end="")
    print("█")
    for n in arr:
        if n == 2 or n == 3 or n == 6 or n == 7 or n == 10 or n == 11 or n == 15:
            print("█ ", end="")
        else:
            print("  ", end="")
    print("█")
    for n in arr:
        if n == 1 or  n == 3 or  n == 5 or  n == 7 or  n == 9 or  n == 11 or  n == 13 or  n == 15:
            print("██", end="")
        else:
            print("  ", end="")
    print("█")