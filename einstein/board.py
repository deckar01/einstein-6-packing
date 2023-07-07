from .config import COLORS
from .utils import color, neighbors
from .weight import norm, W0, W1


class Board:
    def __init__(self):
        self.cells = set()
        self.perimeter = set()
        self.history = []
        self.ihistory = []
        self.score = None

    def marker(self, p):
        if p in self.cells:
            i, n = self._id_cache[p]
            c = COLORS[i + 1]
            v = ' ' if n else '+'
            return f'\033[48;2;{c}m{v}\033[0m'
        else:
            return ' '
    
    def __str__(self):
        self._id_cache = {
            p: (i, n)
            for i, h in zip(self.ihistory, self.history)
            for n, p in enumerate(h)
        }
        L = min(x for x, y in self.perimeter)
        R = max(x for x, y in self.perimeter)
        T = min(y for x, y in self.perimeter)
        B = max(y for x, y in self.perimeter)
        return '\n'.join(
            ''.join(self.marker((x, y)) for x in range(L, R + 1))
            for y in range(T, B + 1)
        )

    def __hash__(self):
        return hash(tuple(sorted(self.cells)))

    def valid(self, tile):
        # Assume tiles have been offset to valid positions
        # Prevent overlapping tiles
        return not any((t in self.cells) for t in tile)

    def add(self, tile, i):
        self.history.append(tile)
        self.ihistory.append(i)
        for t in tile:
            self.perimeter.discard(t)
            assert t not in self.cells, f'{t}'
            self.cells.add(t)
        for t in tile:
            for n in neighbors(t):
                if n not in self.cells:
                    self.perimeter.add(n)
        # TODO: Optimize score change
        self.score = self._score()

    # def remove(self, tile):
    #     for t in tile:
    #         self.cells.remove(t)
    #     for t in tile:
    #         for n in neighbors(t):
    #             if not any((m in self.cells) for m in neighbors(n)):
    #                 self.perimeter.discard(n)
    #         if any((n in self.cells) for n in neighbors(t)):
    #             self.perimeter.add(t)

    # def undo(self):
    #     self.remove(self.history.pop())

    def _score(self):
        total = [0, 0]
        for p in self.perimeter:
            a = color(p)
            for n in neighbors(p):
                if n in self.cells:
                    p = color(n)
                    total[0] += W0[a][p]
                    total[1] += W1[a][p]
        return norm(total) / len(self.history)
    
    def copy(self):
        b = Board()
        b.cells = set(self.cells)
        b.perimeter = set(self.perimeter)
        b.history = list(self.history)
        b.ihistory = list(self.ihistory)
        b.score = self.score
        return b
