import re

rules = {}

class Rule:
    pass

class Sequence:

    def __init__(self, ri):
        self.ri = [int(r) for r in ri]

    def __str__(self):
        return "[{}]".format(self.ri)

    def exec(self, input):
        check = [input]
        for r in self.ri:
            next = []
            for c in check:
                next.extend(rules[str(r)].exec(c))
            check = next
        return check

class Match:

    def __init__(self, value):
        self.value = value

    def exec(self, input):
        if len(input) > 0 and input[0] == self.value:
            return [input[1:]]
        return []

class Option(Rule):

    def __init__(self, sequences):
        self.sequences = [s for s in sequences]

    def exec(self, input):
        res = []
        for seq in self.sequences:
            res.extend(seq.exec(input))
        return res

def read(file):
    with open(file) as f:
        while (line := f.readline().strip()) != "":
            idx, rule = line.split(": ")
            if (m := re.match("\"(.)\"", rule)):
                rules[idx] = Match(m[1])
            else:
                rules[idx] = Option(Sequence(opt.split()) for opt in rule.split("|"))

        return [line.strip() for line in f.readlines()]

def partone():
    input = read("day19a.dat")
    total = 0
    for inp in input:
        if rules["0"].exec(inp) == [""]:
            total += 1
    return total

def parttwo():
    input = read("day19b.dat")
    total = 0
    for inp in input:
        if "" in rules["0"].exec(inp) :
            total += 1
    return total

print(partone())
print(parttwo())
