from collections import defaultdict

from einstein.board import Board
from einstein.tiles import TILES
from einstein.utils import canon, delta, offset


def gen(b):
    M = []

    for i, T in enumerate(TILES):
        P = defaultdict(list)
        for p in b.perimeter:
            P[canon(p)].append(p)
        D = set(
            delta(t, p)
            for t in T
            for p in P[canon(t)]
        )
        V = [
            t
            for d in D
            if b.valid(t := offset(T, d))
        ]
        for v in V:
            n = b.copy()
            n.add(v, i)
            M.append(n)

    return M

try:
    b = Board()
    b.add(TILES[0], 0)
    M = [b]
    stats = {1: 1.0}

    for i in range(2, 20):
        N = (
            n
            for m in M
            for n in gen(m)
        )
        # TODO: dedupe boards
        L = None
        M = set()
        for n in N:
            # Cull heuristic
            if n.score <= stats[i - 1] * 1.0:
                M.add(n)
                if not L or n.score < L:
                    L = n.score
                    stats[i] = [L]
                if n.score == L:
                    print(n, flush=True)
                    print(i, n.score, sep='\t', flush=True)
        stats[i] = L
        print('-------------', flush=True)
except KeyboardInterrupt:
    pass
print()
for i, L in stats.items():
    print(i, L, sep='\t', flush=True)
