import re
import math

def generate_graph(file):
    with open(file, "r") as f:
        for rule in [line.rstrip() for line in f.readlines()]:
            match = re.match("(.*)\s+bags contain\s+(.*)", rule)
            f = match[1]
            if match[2] == "no other bags.":
                yield(f, 0, None)
            for count, to, _ in re.findall("(\d+)\s+([\s\w]+)\s+(bag)[s]?[,.]", match[2]):
                yield(f, int(count), to)

def partone():

    edges = []
    for f, c, t in generate_graph("day7.dat"):
        edges.append((f,t))

    search = ["shiny gold"]
    done = {}

    count = 0
    while len(search) > 0:
        check = search.pop()
        for f,t in edges:
            if t == check and f not in done:
                done[f] = 1
                search.append(f)
                count += 1

    return count

def search(edges, target):
    res = 0
    for f,c,t in edges:
        if f == target and t is not None:
            res += c + c * search(edges, t)
    return res

def parttwo():

    edges = []
    for f, c, t in generate_graph("day7.dat"):
        edges.append((f,c,t))

    return search(edges, "shiny gold")

print(parttwo())
