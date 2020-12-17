def read(file):
    with open(file) as f:
        return [int(n) for n in f.readline().strip().split(",")]

def partone():
    mem = {}
    last = 0
    turn = 1
    next = 0

    for n in read("day15.dat"):
        mem[n] = [ turn ]
        turn += 1
        last = n

    print(mem)

    for i in range(2020 - len(mem)):
        if len(mem[last]) == 1:
            next = 0
        else:
            next = mem[last][1] - mem[last][0]

        mem[next] = mem.get(next, [])
        mem[next].append(turn)
        mem[next] = mem[next][-2:]

        turn += 1
        last = next

    return last

def parttwo():
    mem = {}
    last = 0
    turn = 1
    next = 0

    for n in read("day15.dat"):
        mem[n] = [ -1, turn ]
        turn += 1
        last = n

    print(mem)

    for i in range(30000000 - len(mem)):
        if mem[last][0] == -1:
            next = 0
        else:
            next = mem[last][1] - mem[last][0]

        if next not in mem:
            mem[next] = [-1, turn]
        else:
            mem[next][0] = mem[next][1]
            mem[next][1] = turn

        turn += 1
        last = next

    print(len(mem))

    return last

print(partone())
print(parttwo())
