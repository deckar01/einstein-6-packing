


A = (1, 0)
B = (0, 1)
C = (2, 0)

# Color-color edge length weight
W0 = ( # r * sqrt(3) / 4
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 2, 0, 1, 0, 0),
    (0, 2, 0, 2, 0, 0, 0),
    (0, 0, 2, 0, 0, 0, 1),
    (0, 1, 0, 0, 0, 2, 0),
    (0, 0, 0, 0, 2, 0, 2),
    (0, 0, 0, 1, 0, 2, 0),
)
W1 = ( # r / 2
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 1, 0),
    (0, 0, 0, 0, 1, 0, 1),
    (0, 1, 0, 0, 0, 1, 0),
    (0, 0, 1, 0, 0, 0, 1),
    (0, 1, 0, 1, 0, 0, 0),
    (0, 0, 1, 0, 1, 0, 0),
)


class Board:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.rows = [
            [0 for _ in range(width)]
            for _ in range(height)
        ]
    
    def __str__(self):
        return '\n'.join(
            ''.join(str(v or '.') for v in row)
            for row in self.rows
        ) 

    def get(self, x, y):
        if x < 0 or x >= self.width:
            return 0
        if y < 0 or y >= self.height:
            return 0
        return self.rows[y][x]

    def check(self, tile, position):
        X, Y = position
        for y in range(tile.height):
            for x in range(tile.width):
                if t := tile.rows[y][x]:
                    assert not self.rows[X + x][Y + y]
                    assert t == (s := self.color(X + x, Y + y)), f'{t} != {s} @ {(X + x, Y + y)}'

    def add(self, tile, position):
        X, Y = position
        for y in range(tile.height):
            for x in range(tile.width):
                if t := tile.rows[y][x]:
                    self.rows[Y + y][X + x] = t

    def color(self, x, y):
        i = 1 if y % 2 < 1 else 4
        j = 0 if y % 4 < 2 else 3
        k = (x + j) // 2
        return i + (k % 3)

    def score(self):
        total = [0, 0]
        for y in range(-1, self.height):
            for x in range(-1, self.width):
                a = self.get(x, y)
                b = self.get(x, y + 1)
                if a and not b:
                    p = self.color(x, y + 1)
                    total[0] += W0[a][p]
                    total[1] += W1[a][p]
                elif not a and b:
                    p = self.color(x, y)
                    total[0] += W0[b][p]
                    total[1] += W1[b][p]
                c = self.get(x + 1, y)
                if a and not c:
                    p = self.color(x + 1, y)
                    total[0] += W0[a][p]
                    total[1] += W1[a][p]
                elif not a and c:
                    p = self.color(x, y)
                    total[0] += W0[c][p]
                    total[1] += W1[c][p]
        return total[1] / 2 + total[0] * (3 ** 0.5) / 4


class Tile:
    def __init__(self, offset, *rows):
        self.offset = offset
        self.rows = rows
        self.height = len(self.rows)
        self.width = len(self.rows[0])


T = (
    Tile(
        (0, 0),
        (0, 0, 0, 0, 3, 3, 1, 1, 0),
        (4, 4, 5, 5, 6, 6, 4, 4, 0),
        (0, 0, 0, 0, 0, 2, 2, 3, 3),
    ),
    Tile(
        (0, 0),
        (1, 1, 0, 0, 0, 0, 0),
        (4, 4, 5, 5, 6, 6, 0),
        (0, 3, 3, 1, 1, 2, 2),
        (0, 6, 6, 0, 0, 0, 0),
    ),
    Tile(
        (2, 0),
        (0, 0, 0, 0, 1, 1, 2, 2),
        (5, 5, 6, 6, 4, 4, 5, 5),
        (0, 0, 0, 2, 2, 3, 3, 0),
    ),
    Tile(
        (3, 3),
        (4, 4, 5, 5, 0, 0, 0, 0, 0),
        (0, 3, 3, 1, 1, 2, 2, 3, 3),
        (0, 6, 6, 4, 4, 0, 0, 0, 0),
    ),
    Tile(
        (2, 0),
        (0, 0, 0, 0, 1, 1, 0),
        (5, 5, 6, 6, 4, 4, 0),
        (0, 1, 1, 2, 2, 3, 3),
        (0, 0, 0, 0, 0, 6, 6),
    ),
    Tile(
        (2, 3),
        (0, 4, 4, 5, 5, 0, 0, 0),
        (2, 2, 3, 3, 1, 1, 2, 2),
        (5, 5, 6, 6, 0, 0, 0, 0),
    ),
)

M = (
    (+6, +0),
    (-6, +0),
    (+0, +4),
    (+0, -4),
    (+3, +2),
    (-3, +2),
    (+3, -2),
    (-3, -2),
)

# # Preview board coloring
# for y in range(8):
#     print([P(x, y) for x in range(12)])

# Preview tile perimeter lengths
b = Board(20, 16)
b.check(T[0], (0, 4))
b.add(T[0], (0, 4))
b.check(T[5], (8, 3))
b.add(T[5], (8, 3))
print(b)
print(b.score())
