import re

def count(word, char):
    res = {}
    for c in word:
        res[c] = res.get(c, 0) + 1
    return res.get(char, 0)

def partone():
    valid = 0
    # eg 2-8 t: pncmjxlvckfbtrjh
    pattern = re.compile("(\d+)\-(\d+)\s(.): (.*)")
    with open("day2.dat", "r") as f:
        for m in [pattern.match(l) for l in f.readlines()]:
            (min, max, char, pwd) = (int(m[1]), int(m[2]), m[3] ,m[4])
            total = count(pwd, char)
            if total >= min and total <= max:
                valid += 1
    return valid

def check(word, char, idx):
    return 1 if word[idx - 1] == char else 0

def parttwo():
    valid = 0
    # eg 2-8 t: pncmjxlvckfbtrjh
    pattern = re.compile("(\d+)\-(\d+)\s(.): (.*)")
    with open("day2.dat", "r") as f:
        for m in [pattern.match(l) for l in f.readlines()]:
            (first, second, char, pwd) = (int(m[1]), int(m[2]), m[3] ,m[4])
            if check(pwd, char, first) + check(pwd, char, second) == 1:
                valid += 1
    return valid


print(parttwo())
