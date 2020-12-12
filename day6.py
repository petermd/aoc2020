def generate_records(file):
    people, answers = 0, {}
    with open(file, "r") as f:
        for line in [l.rstrip() for l in f.readlines()]:
            if line == "":
                yield people, answers
                people, answers = 0, {}
                continue
            people += 1
            for q in line:
                answers[q] = 1 + answers.get(q, 0)
    yield people, answers

def partone():
    total = 0
    for people, answers in generate_records("day6.dat"):
        print(people, answers)
        total += len(answers)
    return total

def unanimous(people, answers):
    total = 0
    for question in answers:
        if answers.get(question) == people:
            total += 1
    return total

def parttwo():
    total = 0
    for people, answers in generate_records("day6.dat"):
        total += unanimous(people, answers)
    return total

print(parttwo())
