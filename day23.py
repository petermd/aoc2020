import math


def modone(value, delta, length):
    return modzero(value - 1, delta, length) + 1


def modzero(value, delta, length):
    return ( value - 1 + length ) % length


class Arc:

    def __init__(self, values):
        self.data = values
        self.next = None
        self.cursor = 0

    def inc(self):
        self.cursor += 1
        if self.cursor >= len(self.data):
            self.cursor = 0
            while len(self.next.data) == 0:
                self.next = self.next.next
            next = self.next
            next.cursor = 0
            return next
        return self

    def read(self, v, count):
        start = self.data.index(v)
        res = self.data[start:start+count]
        if len(res) < count:
            res += self.next.read(self.next.data[0], count - len(res))
        return res

    def insert(self, v, values):
        idx = self.data.index(v)
        if idx < self.cursor:
            self.cursor += len(values)
        self.data[idx+1:idx+1] = values
        return idx + 1

    def splice(self, start, count):
        end = min(start + count, len(self.data))
        res = self.data[start:end]
        del self.data[start:end]
        if start < self.cursor:
            self.cursor -= len(res)
        if len(res) < count:
            res += self.next.splice(0, count - len(res))
        return res

    def split(self):
        cut = len(self.data) // 2
        next_arc = Arc(self.data[cut:])
        del self.data[cut:]
        next_arc.next = self.next
        self.next = next_arc
        return next_arc


class Ring:

    def __init__(self, values, arc_length = 200):
        self.first = None
        self.arc_idx = {}
        self.max = len(values)
        self.max_arc = arc_length * 2
        start = 0
        last = None
        while start < len(values):
            arc_data = values[start:start+arc_length]
            cur = Arc(arc_data)
            for v in arc_data:
                self.arc_idx[v] = cur
            if self.first is None:
                self.first = cur
            else:
                last.next = cur
            last = cur
            start += arc_length
        last.next = self.first

    def to_number(self):
        arc = self.arc_idx[1]
        return "".join([str(n) for n in arc.read(1, 9)][1:])

    def next_two(self):
        arc = self.arc_idx[1]
        return arc.read(1, 3)[1:]

    def dump(self):
        print("dump-ring")
        ca = self.first
        while ca is not None:
            print(ca.data)
            ca = ca.next if ca.next != self.first else None

    def debug(self):
        ca = self.first
        max_arc = 0
        total_arcs = 0
        total = 0
        while ca is not None:
            max_arc = max(max_arc, len(ca.data))
            total_arcs += 1
            total += len(ca.data)
            ca = ca.next if ca.next != self.first else None
        print("debug", total, total_arcs, max_arc)

    def slide(self, moves):
        ci = 0
        ca = self.first
        for i in range(moves):

            if i % 100000 == 0:
                print("moves", i)

            tmp = ca.splice(ca.cursor + 1, 3)

            dv = modone(ca.data[ca.cursor], -1, self.max)
            while dv in tmp:
                dv = modone(dv, -1, self.max)

            da = self.arc_idx[dv]
            di = da.insert(dv, tmp)
            for v in tmp:
                self.arc_idx[v] = da

            if len(da.data) > self.max_arc and da.cursor == 0:
                da = da.split()
                for v in da.data:
                    self.arc_idx[v] = da

            ca = ca.inc()

def inflate(data, size):
    additional = size - len(data)
    data.extend([j + 1 for j in range(len(data), len(data) + additional)])
    return data

def example(moves, size, arc_size=200):
    ring = Ring(inflate([int(i) for i in list("389125467")], size), arc_size)
    ring.slide(moves)
    print(ring.next_two())
    ring.debug()
    return ring.to_number()

def partone():
    ring = Ring([int(i) for i in list("284573961")])
    ring.slide(100)
    return ring.to_number()

def parttwo():
    initial = [int(i) for i in list("284573961")]
    ring = Ring(inflate(initial, 1 * 1000 * 1000))
    ring.slide(10 * 1000 * 1000)
    return math.prod(ring.next_two())

print(partone())
print(parttwo())
