class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def key(self):
        return (self.y << 16) + self.x

    def add(self, oth):
        self.x += oth.x
        self.y += oth.y


DIRECTIONS = {
  "w": Vector(-2, 0),
  "nw": Vector(-1, -1),
  "ne": Vector(+1, -1),
  "e": Vector(+2, 0),
  "se": Vector(+1, +1),
  "sw": Vector(-1, +1)
}

class Board:

    def __init__(self):
        self.data = {}
        self.min = Vector(100, 100)
        self.max = Vector(-100, -100)
        self.cursor = Vector(0, 0)

    def load(self, paths):
        for path in paths:
            cursor = Vector(0, 0)
            for d in path:
                cursor.add(DIRECTIONS[d])
            self.flip(cursor)

    def read(self, pos):
        return self.data.get(pos.key(), "white")

    def write(self, pos, value):
        self.data[pos.key()] = value
        self.update(pos)

    def neighbours(self, pos, value):
        total = 0
        for d in DIRECTIONS.values():
            self.cursor.x = pos.x + d.x
            self.cursor.y = pos.y + d.y
            total += 1 if self.read(self.cursor) == value else 0
        return total

    def flip(self, tile):
        state = self.data.get(tile.key(), "white")
        self.data[tile.key()] = "black" if state == "white" else "white"
        self.update(tile)

    def update(self, tile):
        self.min.x = min(self.min.x, tile.x)
        self.min.y = min(self.min.y, tile.y)
        self.max.x = max(self.max.x, tile.x)
        self.max.y = max(self.max.y, tile.y)

    def totals(self):
        totals = {"white": 0, "black": 0}
        for k in self.data:
            totals[self.data.get(k, "white")] += 1
        return totals


def read(file):
    with open(file) as f:
        while (line := list(f.readline().strip())) != []:
            path = []
            while len(line) > 0:
                c = line.pop(0)
                if c in ['n','s']:
                    path.append(c + line.pop(0))
                else:
                    path.append(c)
            yield path


def partone():
    board = Board()
    board.load(read("day24.dat"))
    return board.totals()["black"]


def parttwo():
    board = Board()
    board.load(read("day24.dat"))

    pos = Vector(0, 0)
    for i in range(100):
        update = Board()
        for y in range(board.min.y - 2, board.max.y + 2):
            for x in range(board.min.x - 2, board.max.x + 2):
                pos.x, pos.y = x, y
                if board.read(pos) == "black":
                    if 1 <= board.neighbours(pos, "black") <= 2:
                        update.write(pos, "black")
                    else:
                        pass
                else:
                    if board.neighbours(pos, "black") == 2:
                        update.write(pos, "black")
        board = update

    return board.totals()["black"]


print(partone())
print(parttwo())
