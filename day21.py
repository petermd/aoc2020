import re


def read(file):
    pattern = re.compile("([\w\s]*)(\(contains )(.*)(\))")
    with open(file) as f:
        while m := pattern.match(f.readline()):
            yield set([w.strip() for w in m[1].split()]), set([w.strip() for w in m[3].split(",")])


def resolve(file):

    ingredients = {}
    allergens = {}
    options = {}
    for ing, all in read(file):
        for i in ing:
            ingredients[i] = ingredients.get(i, 0) + 1
        for a in all:
            if a in options:
                options[a] = options[a].intersection(ing)
            else:
                options[a] = ing

    solutions = [(o, len(options[o])) for o in options]
    while len(solutions) > 0:
        solutions.sort(key = lambda x: x[1])
        i = solutions.pop(0)[0]
        ing = options[i].pop()
        for idx, s in enumerate(solutions):
            if ing in options[s[0]]:
                options[s[0]].remove(ing)
                solutions[idx] = (s[0], s[1]-1)
        allergens[i] = ing

    return ingredients, allergens


def partone():
    ingredients, allergens = resolve("day21.dat")
    return sum([ingredients[i] for i in ingredients if i not in allergens.values()])


def parttwo():
    ingredients, allergens = resolve("day21.dat")
    dangerous_ingredients = {}
    for k, v in allergens.items():
        dangerous_ingredients[v] = k
    res = [k for k in dangerous_ingredients.keys()]
    res.sort(key = lambda x: dangerous_ingredients[x])
    return ",".join(res)


print(partone())
print(parttwo())
