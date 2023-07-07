from einstein.board import Board
from einstein.tiles import TILES
from einstein.utils import canon, offset


b = Board()

assert b.valid(TILES[0])
b.add(TILES[0])

print(b)
print(b.score())

m = offset(TILES[5], (6, -4))
assert b.valid(m)
b.add(m)

print(b)
print(b.score())

b.undo()

print(b)
print(b.score())
