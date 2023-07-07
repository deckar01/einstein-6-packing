def neighbors(p):
    x, y = p
    return (
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    )

def color(p):
    x, y = p
    i = 1 if y % 2 < 1 else 4
    j = 0 if y % 4 < 2 else 3
    k = (x + j) // 2
    return i + (k % 3)

def canon(p):
    x, y = p
    i = 1 if y % 2 < 1 else 7
    j = 0 if y % 4 < 2 else 3
    k = (x + j)
    return i + (k % 6)

def offset(tile, p):
    x, y = p
    return tuple(
        (x + i, y + j)
        for i, j in tile
    )
