import re

def read(file):
    pattern = re.compile("(mem)\[(\d*)\]")
    with open(file) as f:
        for op in [l.strip().split("=") for l in f.readlines()]:
            if op[0].strip() == "mask":
                yield "mask", "*", op[1].strip()
            else:
                m = pattern.match(op[0])
                yield "set", int(m[2]), int(op[1])

def parse_mask(s):
    mask = 0x0
    over = 0x0
    floating = 0x0
    for i in range(len(s)):
        mask <<= 1
        over <<= 1
        floating <<= 1
        if s[i] == '1':
            mask |= 0x1
            over |= 0x1
        elif s[i] == '0':
            mask |= 0x0
        elif s[i] == 'X':
            mask |= 0x1
            floating |= 0x1

    return ~    mask, over, floating

def partone():

    mask = 0x0
    over = 0x0
    mem = {}

    for op, addr, value in read("day14.dat"):
        if op == "mask":
            mask, over, _ = parse_mask(value)
        elif op == "set":
            mem[addr] = (mask & value) | over

    return sum(mem.values())

def generate_seq(num):
    perm = [ 0x0 ]
    check = 1
    while(check <= num):
        if check & num:
            perm = [v | check for v in perm] + perm
        check <<=1
    return perm

def parttwo():

    mask = 0x0
    over = 0x0
    floating = 0x0
    mem = {}

    for op, addr, value in read("day14.dat"):
        if op == "mask":
            mask, over, floating = parse_mask(value)
        elif op == "set":
            for ma in generate_seq(floating):
                mem[(addr & mask) | over | ma] = value

    return sum(mem.values())

print(partone())
print(parttwo())
