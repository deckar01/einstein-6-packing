from .config import COLORS
from .utils import color, neighbors
from .weight import norm, W0, W1


class Board:
    def __init__(self):
        self.cells = set()
        self.perimeter = set()
        self.history = []

    def marker(self, p):
        c = COLORS[color(p)]
        if p in self.cells:
            v = '█'
        elif p in self.perimeter:
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
            ''.join(self.marker((x, y)) for x in range(L, R + 1))
            for y in range(T, B + 1)
        )

    def valid(self, tile):
        # Assume tiles have been offset to valid positions
        # Prevent overlapping tiles
        if any(t in self.cells for t in tile):
            return False
        # Allow placing the first tile anywhere
        if not self.perimeter:
            return True
        # Require tiles to touch
        return any(t in self.perimeter for t in tile)

    def add(self, tile):
        self.history.append(tile)
        for t in tile:
            self.perimeter.discard(t)
            self.cells.add(t)
        for t in tile:
            for n in neighbors(t):
                if n not in self.cells:
                    self.perimeter.add(n)

    def remove(self, tile):
        for t in tile:
            self.cells.remove(t)
        for t in tile:
            for n in neighbors(t):
                if not any((m in self.cells) for m in neighbors(n)):
                    self.perimeter.discard(n)
            if any((n in self.cells) for n in neighbors(t)):
                self.perimeter.add(t)

    def undo(self):
        self.remove(self.history.pop())

    def score(self):
        total = [0, 0]
        for p in self.perimeter:
            a = color(p)
            for n in neighbors(p):
                if n in self.cells:
                    p = color(n)
                    total[0] += W0[a][p]
                    total[1] += W1[a][p]
        return norm(total)
