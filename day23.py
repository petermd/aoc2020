def modone(value, delta, length):
    return modzero(value - 1, delta, length) + 1


def modzero(value, delta, length):
    return ( value - 1 + length ) % length


class Ring:

    def __init__(self, values, max = None):
        self.data = list(values)
        self.pos = [0] * len(values)
        for idx, v in enumerate(values):
            self.pos[v - 1] = idx
        max = max if max is not None else len(values)
        for i in range(len(values), max):
            self.data.append(i + 1)
            self.pos.append(i)
        self.length = len(self.data)

    def to_number(self):
        idx = self.pos[1 - 1]
        res = []
        for i in range(1, self.length):
            res.append(str(self.data[(idx + i) % self.length]))
        return "".join(res)

    def slide(self, moves):
        ci = 0
        tmp = [0] * 3

        def rp(v):
            return (v + self.length) % self.length

        for i in range(moves):

            #print(self.data, self.data[ci])

            cv = modone(self.data[ci], -1, self.length)

            di = self.pos[cv - 1]
            while 1<= rp(di - ci) <= 3:
                cv = modone(cv, -1, self.length)
                di = self.pos[cv - 1]

            if i % 1000 == 0:
                print("move", i, di - ci)

            tmp[0] = self.data[rp(ci + 1)]
            tmp[1] = self.data[rp(ci + 2)]
            tmp[2] = self.data[rp(ci + 3)]

            dr = (di - ci + self.length) % self.length
            dl = (ci - di + self.length) % self.length

            if dr < dl:
                self.move(ci + 1, ci + 4, +1, rp(di - ci - 3))
                di = rp(di - 3)
            else:
                self.move(ci + 3, ci, -1, dl)
                ci = rp(ci + 3)

            self.write(di + 1, tmp[0])
            self.write(di + 2, tmp[1])
            self.write(di + 3, tmp[2])

            ci = rp(ci + 1)

    def write(self, pos, val):
        pos = (pos + self.length) % self.length
        self.data[pos] = val
        self.pos[val - 1] = pos

    def move(self, dest, src, inc, len):
        src += self.length
        dest += self.length
        dx = 0
        for i in range(len):
            di = (dest + dx) % self.length
            si = (src + dx) % self.length
            self.data[di] = self.data[si]
            self.pos[self.data[si] - 1] = di
            dx += inc


def sequence():
    ring = Ring([], 30)
    ring.slide(100)

def example(moves):
    ring = Ring([int(i) for i in list("389125467")])
    ring.slide(moves)
    return ring.to_number()

def partone():
    ring = Ring([int(i) for i in list("284573961")])
    ring.slide(100)
    return ring.to_number()

def parttwo():
    ring = Ring([int(i) for i in list("389125467")], 1 * 1000 * 1000)
    ring.slide(10 * 1000)

print(partone())
print(parttwo())
