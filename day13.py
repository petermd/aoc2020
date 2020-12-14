def read(file):
    with open(file) as f:
        now = int(f.readline())
        routes = list(f.readline().rstrip().split(","))
        routes = [(i, int(o)) for i, o in enumerate(routes) if o != 'x']
        return now, routes

def next(now, offset):
    return offset - (now % offset) % offset

def partone():
    now, routes = read("day13.dat")
    offsets = [(r[1], next(now, r[1])) for r in routes]
    offsets.sort(key = lambda x: x[1])
    return offsets[0][0] * offsets[0][1]

def parttwo():
    _, routes = read("day13.dat")
    cur = mult = routes.pop(0)[1]
    while len(routes) > 0:
        r = routes.pop(0)
        delta = r[1] - (r[0] % r[1])
        while(cur % r[1] != delta):
            cur += mult
        mult *= r[1]
    return cur

print(partone())
print(parttwo())
