def partone(file):
    match = [0] * 2020
    with open(file,"r") as f:
        for n in [ int(line) for line in f.readlines() ]:
            if match[2020 - n] == 1:
                return n * (2020 - n)
            match[n] = 1

def find(match, left, start, total, steps):
    if steps == 0:
        return total if left == 0 else 0
    for i in range(start, 0, -1):
        if match[i] and i <= left:
            res = find(match, left - i, min(i - 1, left), total * i, steps - 1)
            if res > 0:
                return res
    return 0

def parttwo(file):
    match = [0] * 2020
    with open(file,"r") as f:
        for n in [ int(line) for line in f.readlines() ]:
            match[n] = 1

    return find(match, 2020, 2019, 1, 3)

print(parttwo("day1.csv"))
