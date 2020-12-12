import math

map = []
with open("day3.dat", "r") as f:
    map = [line.rstrip() for line in f.readlines()]

def slope(ix, iy):
    trees, x, y = 0, 0, 0
    while y < len(map):
        trees += map[y][x % len(map[y])] == '#'
        y += iy
        x += ix
    return trees

def partone():
    return slope(3,1)

def parttwo():
    return math.prod([slope(1, 1), slope(3, 1), slope(5, 1), slope(7, 1), slope(1, 2)])

print(partone())
