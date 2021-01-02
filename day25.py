KEY_MOD = 20201227

def partone():
    #max_loops, cpk, dpk = 100, 5764801, 17807724
    max_loops, cpk, dpk = 100 * 1000 * 1000, 17607508, 15065270

    print("find-loops")
    value = 1
    res = {}
    for i in range(1, max_loops):
        value = (value * 7) % KEY_MOD
        if value == cpk or value == dpk:
            if value in res:
                print("loop-detected")
                break
            res[value] = i

    if pow(cpk, res[dpk], KEY_MOD) == pow(dpk, res[cpk], KEY_MOD):
        print("match", res[cpk], res[dpk], pow(cpk, res[dpk], KEY_MOD))
        return pow(cpk, res[dpk], KEY_MOD)

print(partone())
