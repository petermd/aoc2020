import re
import math
import copy


def read(file):
    with open(file) as f:
        while line := f.readline():
            id = int(re.match("(Tile )(\d*)\:", line.strip())[2])
            data = []
            for y in range(10):
                data.append(list(f.readline().strip()))
            f.readline()
            yield Tile.create(id, data)


def load(tiles, width, height, cfg):

    idx = {}
    for t in tiles:
        idx[t.id] = t

    b = Board(width, height)
    for st in cfg.split(","):
        id, rotations, flips = st.split(":")
        t = idx[int(id)]
        if int(flips) > 0:
            t = t.flip()
        for i in range(int(rotations)):
            t = t.rotate()
        b.add(t)

    print("exp:", cfg)
    print("act:", b.dump())

    return b


class Bitmap:

    def __init__(self, data):
        self.width = len(data[0])
        self.height = len(data)
        self.data = data

    def dump(self):
        for row in self.data:
            print("".join(row))

    def count(self, c):
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.data[y][x] == c:
                    total += 1
        return total

    def find(self, bitmap):
        matches = 0
        for y in range(self.height - bitmap.height):
            for x in range(self.width - bitmap.width):
                if self.match_bitmap(x, y, bitmap):
                    matches += 1
                    self.stamp_bitmap(x, y, bitmap)
        return matches

    def match_bitmap(self, tx, ty, bitmap):
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                if bitmap.data[y][x] != '#':
                    continue
                if self.data[ty + y][tx + x] == '.':
                    return False
        return True

    def stamp_bitmap(self, tx, ty, bitmap):
        for y in range(bitmap.height):
            for x in range(bitmap.width):
                if bitmap.data[y][x] != '#':
                    continue
                self.data[ty + y][tx + x] = 'O'


class Tile:

    def __init__(self, id, data, edges, rotations=0, flips=0):
        self.id = id
        self.rotations = rotations
        self.flips = flips
        self.data = data
        self.edges = edges

    def __str__(self):
        return "{}:{}:{}".format(self.id, self.rotations, self.flips)

    def width(self):
        return len(self.edges[0])

    def draw(self, screen, tx, ty, bw, tw):
        sx = bw // 2
        sy = bw // 2
        for y in range(tw):
            for x in range(tw):
                screen[ty + y][tx + x] = self.data[sy + y][sx + x]

    def match(self, match_edges):
        for idx in range(len(match_edges)):
            if match_edges[idx] and match_edges[idx] != self.edges[idx]:
                return False
        return True

    def rotate(self):
        w, h = len(self.data[0]), len(self.data)
        rot_data = [ ['?'] * w for y in range(w)]
        for y in range(h):
            for x in range(w):
                rot_data[y][x] = self.data[w - 1 - x][y]

        return Tile.create(self.id, rot_data, self.rotations + 1, self.flips)

    def flip(self):
        w, h = len(self.data[0]), len(self.data)
        flip_data = [ ['?'] * w for y in range(w)]
        for y in range(h):
            for x in range(w):
                flip_data[y][x] = self.data[w - 1 - y][x]

        return Tile.create(self.id, flip_data, self.rotations, self.flips + 1)

    def generate(self):
        """ Generate all permutations of this title, rotated and flipped """
        next = copy.copy(self)

        for i in range(4):
            yield next
            next = next.rotate()

        next = self.flip()

        for i in range(4):
            yield next
            next = next.rotate()


    @classmethod
    def create(cls, id, data, rotations = 0, flips = 0):
        edges = [
            data[0],
            [r[-1] for r in data],
            data[-1],
            [r[0] for r in data]
        ]
        return Tile(id, data, edges, rotations, flips)


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = []
        self.tiles = set()

    def __copy__(self):
        nb = Board(self.width, self.height)
        nb.data = copy.copy(self.data)
        nb.tiles = copy.copy(self.tiles)
        return nb

    def draw(self, bw):
        tw = self.data[0].width() - bw
        screen = [[' '] * tw * self.width for y in range(self.height * tw)]
        for idx in range(len(self.data)):
            y = idx // self.width
            x = idx % self.width
            self.data[idx].draw(screen, (x * tw), (y * tw), bw, tw  )
        return screen

    def add(self, tile):
        self.data.append(tile)
        self.tiles.add(tile.id)

    def next(self):
        idx = len(self.data)
        match_edges = [None] * 4
        if idx >= self.width:
            up = self.data[idx - self.width]
            match_edges[0] = up.edges[2]
        if idx % self.width > 0:
            left = self.data[idx - 1]
            match_edges[3] = left.edges[1]
        return match_edges

    def match(self, tiles, match_edges):
        for t in tiles:
            if t.id in self.tiles:
                continue
            if t.match(match_edges):
                return t
        return None

    def full(self):
        return len(self.data) == (self.width * self.height)

    def dump(self):
        img = self.draw(0)
        for row in img:
            print("".join(row))
        print(",".join([str(t) for t in self.data]))

    def corners(self):
        return [
            self.data[0].id,
            self.data[self.width - 1].id,
            self.data[self.width * (self.height - 1)].id,
            self.data[(self.width * self.height) - 1].id
        ]


def partone():

    tiles = []
    for tile in read("day20.dat"):
        tiles.append(tile)

    w = int(math.sqrt(len(tiles)))

    print(len(tiles), "tiles", w)

    all_tiles = []
    for t in tiles:
        for tv in t.generate():
            all_tiles.append(tv)

    options = []
    for t in all_tiles:
        b = Board(w, w)
        b.add(t)
        options.append(b)

    while len(options) > 0:
        b = options.pop(0)
        me = b.next()
        if t := b.match(all_tiles, me):
            b.add(t)
            if b.full():
                b.dump()
                return math.prod(b.corners())
            options.append(b)


def parttwo():

    tiles = []
    for tile in read("day20.dat"):
        tiles.append(tile)

    w = int(math.sqrt(len(tiles)))

    print(len(tiles), "tiles", w)

    b= load(tiles, 12, 12, "3343:3:0,2729:0:1,1531:3:1,1543:0:1,1319:3:1,2851:3:1,3137:3:1,3001:0:1,3673:2:0,3389:1:1,3163:1:1,3677:3:0,2693:1:1,3923:2:1,3571:3:1,2671:1:1,3491:2:0,2161:1:0,2081:3:0,2969:3:0,2131:3:0,1931:1:0,2753:2:1,2003:1:0,1451:2:1,2711:3:1,2213:3:0,2503:1:1,1381:2:1,3701:3:0,1759:3:0,1877:1:0,2713:2:0,1049:2:1,1823:1:1,2179:1:0,3847:3:1,1129:3:0,3019:1:0,1879:2:0,2377:1:0,2311:2:0,1913:1:1,1777:1:0,1789:2:1,2297:0:1,3613:2:0,2339:1:1,2347:1:0,3541:3:1,3917:3:0,3391:3:0,1933:1:0,2203:3:1,1889:2:0,1103:0:1,2903:3:0,3793:0:1,1163:1:1,1327:3:1,1249:1:1,3907:0:1,2411:1:1,3329:2:1,2341:2:0,3853:1:0,1489:2:1,1831:1:1,1607:2:0,3259:2:1,1453:0:1,1481:1:0,2687:2:0,2833:3:0,2437:2:1,3323:2:0,1493:2:0,2879:0:1,1663:3:1,2647:0:1,1259:1:1,2371:1:0,1223:0:1,2683:3:1,2089:3:0,3733:2:1,2579:3:1,3499:1:1,1021:0:1,3803:0:1,2837:2:0,2927:1:1,3767:3:0,1597:1:1,3881:0:1,1973:0:1,3373:2:0,2473:2:0,3631:1:0,1367:1:0,1231:1:1,2521:1:1,3989:3:1,2971:2:1,2441:1:0,1031:1:0,2609:3:0,1283:3:0,2129:2:1,3299:1:0,1483:1:0,2273:3:1,2719:3:0,3533:1:1,1321:1:0,3413:2:0,1867:2:0,3943:1:1,2207:3:1,2593:3:1,1123:0:1,1373:2:0,2153:2:1,3643:1:0,1579:3:1,3593:1:0,2657:3:0,1549:3:0,1811:0:1,2333:3:0,1667:3:1,1871:0:1,3821:2:1,2113:3:1,2039:2:1,3457:2:0,3109:2:0,3889:3:0,3359:2:0,2141:2:0,1999:3:1,3217:1:1,1619:3:0,3709:0:1")
    #b = load(tiles, 3, 3, "1951:1:0,2729:1:0,2971:1:0,2311:1:0,1427:1:0,1489:1:0,3079:1:1,2473:2:0,1171:3:0")

    img = Bitmap(b.draw(2))

    monster = Bitmap([
        list("                  # "),
        list("#    ##    ##    ###"),
        list(" #  #  #  #  #  #   ")
    ])

    print(img.find(monster))
    img.dump()
    return img.count('#')

print(partone())
print(parttwo())
