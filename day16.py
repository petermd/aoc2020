import math

class Condition:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return "{}-{}".format(self.start, self.end)

    def validate(self, num):
        return num >= self.start and num <= self.end

    @classmethod
    def parse(cls, str):
        comp = str.split("-")
        return Condition(int(comp[0].strip()), int(comp[1].strip()))

class Rule:

    def __init__(self, id, conditions):
        self.id = id
        self.conditions = conditions

    def __str__(self):
        return "{}: {}".format(self.id, [str(c) for c in self.conditions])

    def validate(self, num):
        return any([c.validate(num) for c in self.conditions])

def read_rules(f):
    res = []
    while (line := f.readline().strip()) != "":
        tag, rule_str = line.split(":")
        conds = []
        for cond in [s.strip() for s in rule_str.split("or")]:
            conds.append(Condition.parse(cond))
        res.append(Rule(tag, conds))
    return res

def read_tickets(f):
    f.readline()
    tickets = []
    while (line := f.readline().strip()) != "":
        fields = line.split(",")
        tickets.append([int(f) for f in fields])
    return tickets

def read(file):
    with open(file) as f:
        rules = read_rules(f)
        my_ticket = read_tickets(f)[0]
        nearby_tickets = read_tickets(f)
        return rules, my_ticket, nearby_tickets

def matching_rules(rules, num):
    res = []
    for r in rules:
        if r.validate(num):
            res.append(r.id)
    return res

def partone():
    rules, my_ticket, nearby_tickets = read("day16.dat")

    print([str(r) for r in rules])

    res = 0
    for t in nearby_tickets:
        for f in t:
            res += f if len(matching_rules(rules, f)) == 0 else 0

    return res

def invalid(rules, t):
    for f in t:
        if len(matching_rules(rules, f)) == 0:
            return True
    return False

def generate_valid(perms):
    """
    Generate all valid combinations for a given set of permutations
    """
    opts = []
    for id in perms[0]:
        opts.append([ id ])

    max = 0
    while len(opts) > 0:
        next = opts.pop(0)
        if len(next) > max:
            max = len(next)
        for id in perms[len(next)]:
            if id not in next:
                if len(next) + 1 == len(perms):
                    yield next[:] + [id]
                else:
                    opts.append(next[:] + [id])

def calc_combinations(label, fields):
    total_comb = 0
    for vf in fields:
        comb = [ len(f) for f in vf ]
        total_comb += math.prod(comb)
    print(label, total_comb)

def solve(fields):

    candidates = [(i, len(fields[i])) for i in range(len(fields))]
    candidates.sort(key = lambda x: x[1])

    print("total", [len(fields[c[0]]) for c in candidates])

    idx = 0
    while idx < len(fields) and len(fields[candidates[idx][0]]) == 1:
        target = fields[candidates[idx][0]]
        for i in range(len(fields)):
            if i == candidates[idx][0]:
                continue
            fields[i] = [f for f in fields[i] if f not in target]
        idx += 1

    print("candidates", [len(fields[c[0]]) for c in candidates])

def parttwo():
    rules, my_ticket, nearby_tickets = read("day16.dat")

    print([str(r) for r in rules])

    valid_tickets = [t for t in nearby_tickets if not invalid(rules, t)]

    valid_fields = []

    for t in valid_tickets:
        fields = [ matching_rules(rules, f) for f in t ]
        valid_fields.append(fields)

    calc_combinations("total_comb", valid_fields)

    # Filter columns
    common_fields = [ set(valid_fields[0][i]) for i in range(len(valid_fields[0])) ]
    for i in range(1, len(valid_tickets)):
        for j in range(len(common_fields)):
            common_fields[j] = common_fields[j] & set(valid_fields[i][j])

    solve(common_fields)

    for i in range(len(valid_tickets)):
        for j in range(len(common_fields)):
            valid_fields[i][j] = [f for f in valid_fields[i][j] if f in common_fields[j]]

    calc_combinations("filtered_comb", valid_fields)

    opts = {}
    for vf in valid_fields:
        for opt in generate_valid(vf):
            key = ":".join(opt)
            opts[key] = opts.get(key, 0) + 1

    print("found", len(opts), len(valid_tickets))

    for i, (k,v) in enumerate(opts.items()):
        if v == len(valid_tickets):
            total = 1
            for i, k in enumerate(k.split(":")):
                if k.startswith("departure"):
                    total *= my_ticket[i]
            return total

print(partone())
print(parttwo())
