import re

code = []

parse = re.compile("(\w{3})\s\+?(.*)")
with open("day8.dat", "r") as f:
    for cmd in [l.rstrip() for l in f.readlines()]:
        m = parse.match(cmd)
        code.append((m[1], int(m[2])))

def exec(code):
    acc = 0
    ip = 0
    loop = {}
    while(ip < len(code)):
        if ip in loop:
            return "lock", acc
        loop[ip] = 1
        if code[ip][0] == "acc":
            acc += code[ip][1]
        elif code[ip][0] == "jmp":
            ip += code[ip][1]
            continue
        ip += 1

    return "finish", acc

def partone():
    return exec(code)

def parttwo():
    for idx in range(len(code)):
        if code[idx][0] == "nop" and code[idx][1] != 0:
            mut = code.copy()
            mut[idx] = ("jmp", mut[idx][1])
        elif code[idx][0] == "jmp":
            mut = code.copy()
            mut[idx] = ("nop", 0)
        res = exec(mut)
        if res[0] == "finish":
            return res[1]


print(parttwo())
