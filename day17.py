import math

class Vector:

    TWOD = ["x", "y"]
    THREED = ["x","y","z"]
    FOURD = ["x","y","z","w"]

    def __init__(self, dim, data = None):
        self.dim = dim
        self.data = data if data is not None else [0] * len(dim)

    def __str__(self):
        return "({})".format(self.data)

    def smaller(self):
        return Vector(self.dim, [n - 1 for n in self.data])

    def bigger(self):
        return Vector(self.dim, [n + 1 for n in self.data])

    def clamp_lower(self, other):
        self.data = [min(self.data[i], other.data[i]) for i in range(len(self.dim))]

    def clamp_higher(self, other):
        self.data = [max(self.data[i], other.data[i]) for i in range(len(self.dim))]

    def neighbours(self):
        ld = len(self.dim)
        offset = [0] * ld
        for i in range(pow(3, ld)):
            for j in range(ld):
                offset[j] = (i % 3) - 1
                i //= 3
            if not any(offset):
                continue
            yield Vector(self.dim, [self.data[j] + offset[j] for j in range(ld)])

    @classmethod
    def range(cls, start, end):
        diff = [end.data[i] - start.data[i] + 1 for i in range(len(start.dim))]
        cursor = Vector(start.dim, [0] * len(start.dim))
        for i in range(math.prod(diff)):
            for j in range(len(start.dim)):
                cursor.data[j] = start.data[j] + (i % diff[j])
                i //= diff[j]
            yield cursor

    @classmethod
    def add(cls, a, b):
        return Vector(a.dim, [a.data[i] + b.data[i] for i in len(a.data)])


class SparseBoard:

    def __init__(self, dim):
        self.data = {}
        self.dim = dim
        self.min = Vector(dim, [0] * len(dim))
        self.max = Vector(dim, [0] * len(dim))

    def active(self):
        return sum([self.read(cursor) for cursor in Vector.range(self.min, self.max)])

    def neighbours(self, loc):
        return sum([self.read(cursor) for cursor in loc.neighbours()])

    def read(self, loc):
        return self.data.get(str(loc), 0)

    def write(self, loc, value):
        self.min.clamp_lower(loc)
        self.max.clamp_higher(loc)
        self.data[str(loc)] = value

    def dump(self):
        start = self.min
        end = self.max
        cursor = Vector(start.dim, start.data.copy())
        print("dump", start, end)
        for z in range(end.data[2] - start.data[2] + 1):
            print("z=", start.data[2] + z)
            for y in range(end.data[1] - start.data[1] + 1):
                cursor.data[1] = y
                row = ""
                for x in range(end.data[0] - start.data[0] + 1):
                    cursor.data[0] = x
                    row += '#' if self.read(cursor) else '.'
                print(row)


def read(file, dim):
    board = SparseBoard(dim)
    with open(file) as f:
        cursor = Vector(dim)
        for str in [l.strip() for l in f.readlines()]:
            for x in range(len(str)):
                cursor.data[0] = x
                board.write(cursor, 1 if str[x] == '#' else 0)
            cursor.data[1] += 1
    return board


def execute(board, cycles):

    for cycle in range(cycles):

        next = SparseBoard(board.dim)

        for cursor in Vector.range(board.min.smaller(), board.max.bigger()):
            if board.read(cursor):
                if 2 <= board.neighbours(cursor) <= 3:
                    next.write(cursor, 1)
            else:
                if board.neighbours(cursor) == 3:
                    next.write(cursor, 1)
        board = next

        print("turn", cycle + 1, "active", board.active())

    return board.active()


def partone():

    board = read("day17.dat", Vector.THREED)
    print("start", board.active())

    return execute(board, 6)


def parttwo():

    board = read("day17.dat", Vector.FOURD)
    print("start", board.active())

    return execute(board, 6)


print(partone())
print(parttwo())
