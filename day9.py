def generate_data(file):
    with open(file, "r") as f:
        for l in f.readlines():
            yield int(l.strip())

def sums_to(data, target):

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] + data[j] == target:
                return True

    return False

def partone():
    window = 25
    ci = 0
    data = [0] * window

    for n in generate_data("day9.dat"):
        if ci >= window:
            if not sums_to(data, n):
                return n
        ci += 1
        data[ci % window] = n

def check(data, end, size, agg, target):
    start = ( end + len(data) - size ) % len(data)
    while agg >= target:
        if agg == target:
            if start > end:
                return data[:end] + data[start:]
            else:
                return data[start:end+1]
        agg -= data[start]
        start = (start + 1) % len(data)
    return None

def parttwo():

    target = 20874512
    window = 100
    ci = 0
    data = [0] * window
    rolling_agg = 0

    for n in generate_data("day9.dat"):
        rolling_agg -= data[ci % window]
        rolling_agg += n
        data[ci % window] = n
        res = check(data, ci % window, min(ci, window), rolling_agg, target)
        if res:
            res = sorted(res)
            return res[0], res[-1], res, res[0] + res[-1]
        ci += 1

print(partone())
