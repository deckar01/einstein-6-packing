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

def neighbors(x, y):
    return (
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
    )

def color(x, y):
    i = 1 if y % 2 < 1 else 4
    j = 0 if y % 4 < 2 else 3
    k = (x + j) // 2
    return i + (k % 3)

class Board:
    def __init__(self):
        self.cells = set()
        self.perimeter = set()

    def marker(self, x, y):
        C = [
            '0;0;0',
            '0;208;108',
            '98;89;249',
            '211;210;211',
            '68;67;68',
            '68;255;0',
            '207;9;0',
        ]
        c = C[color(x, y)]
        if (x, y) in self.cells:
            v = '█'
        elif (x, y) in self.perimeter:
            v = '+'
        else:
            v = ' '
        return f'\033[38;2;{c}m{v}\033[0m'
    
    def __str__(self):
        L = min(x for x, y in self.perimeter)
        R = max(x for x, y in self.perimeter)
        T = min(y for x, y in self.perimeter)
        B = max(y for x, y in self.perimeter)
        return '\n'.join(
            ''.join(self.marker(x, y) for x in range(L, R + 1))
            for y in range(T, B + 1)
        )

    def check(self, tile, position):
        X, Y = position
        for x, y in tile:
            if t := color(x, y):
                assert (X + x, Y + y) not in self.cells
                assert t == (s := color(X + x, Y + y)), f'{t} != {s} @ {(X + x, Y + y)}'

    def add(self, tile, position):
        X, Y = position
        for x, y in tile:
            a = (X + x, Y + y)
            self.perimeter.discard(a)
            self.cells.add(a)
        for x, y in tile:
            for n in neighbors(X + x, Y + y):
                if n not in self.cells:
                    self.perimeter.add(n)

    def remove(self, tile, position):
        X, Y = position
        for x, y in tile:
            for n in neighbors(X + x, Y + y):
                self.perimeter.discard(n)
        for x, y in tile:
            self.cells.remove((X + x, Y + y))
        for x, y in tile:
            if any((n in self.cells) for n in neighbors(X + x, Y + y)):
                self.perimeter.add((X + x, Y + y))

    def score(self):
        total = [0, 0]
        for x, y in self.perimeter:
            a = color(x, y)
            for nx, ny in neighbors(x, y):
                if (nx, ny) in self.cells:
                    p = color(nx, ny)
                    total[0] += W0[a][p]
                    total[1] += W1[a][p]
        return total[1] / 2 + total[0] * (3 ** 0.5) / 4


T = (
    (
                                    (4,0), (5,0), (6,0), (7,0),
        (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1),
                                           (5,2), (6,2), (7,2), (8,2),
    ),
    (
        (0,0), (1,0),
        (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),
               (1,2), (2,2), (3,2), (4,2), (5,2), (6,2),
               (1,3), (2,3),
    ),
    (
                                    (6,0), (7,0), (8,0), (9,0),
        (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1),
                             (5,2), (6,2), (7,2), (8,2),
    ),
    (
        (0,1), (1,1), (2,1), (3,1),
               (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2),
               (1,3), (2,3), (3,3), (4,3),
    ),
    (
                                    (6,0), (7,0),
        (2,1), (3,1), (4,1), (5,1), (6,1), (7,1),
               (3,2), (4,2), (5,2), (6,2), (7,2), (8,2),
                                           (7,3), (8,3),
    ),
    (
               (3,3), (4,3), (5,3), (6,3),
        (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4),
        (2,5), (3,5), (4,5), (5,5),
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


# Preview tile perimeter lengths
b = Board()
b.check(T[0], (0, 0))
b.add(T[0], (0, 0))
b.check(T[5], (6, -4))
b.add(T[5], (6, -4))
print(b)
print(b.score())
# b.remove(t, (0, 0))
# print(b.perimeter)
