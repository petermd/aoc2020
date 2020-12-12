data = []
with open("day10.dat") as f:
    for n in [int(line.rstrip()) for line in f.readlines()]:
        data.append(n)

def partone(data):
    data = sorted(data)
    counts = [0] * 4
    last = 0
    for i in range(len(data)):
        diff = data[i] - last
        counts[diff] += 1
        last = data[i]
    counts[3] += 1
    return counts[1] * counts[3]


def parttwo(data):
    data = [0] + sorted(data)
    path = { (data[-1] + 3) : 1 }
    while(len(data) > 0):
        n = data.pop()
        path[n] = sum([path.get(n + idx + 1, 0) for idx in range(3)])
    return path[0]


print(parttwo(data))
