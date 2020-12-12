def generate_instructions(file):
    with open(file) as f:
        for l in f.readlines():
            yield l[0], int(l[1:])

class Vector:

    def __init__(self, sx, sy):
        self.x = sx
        self.y = sy

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def manhattan_distance(self, sx, sy):
        return abs(sx - self.x) + abs (sy - self.y)

    def project(self, wp, dist):
        self.x += wp.x * dist
        self.y += wp.y * dist

    def pivot(self, ang, dir):
        for turns in range((ang % 360) // 90):
            self.x, self.y = -dir * self.y, dir * self.x

COMPASS = {
    "N": Vector(0 ,-1),
    "S": Vector(0, +1),
    "E": Vector(1, 0),
    "W": Vector(-1, 0)
}

def partone():
    ship = Vector(0, 0)
    heading = Vector(1, 0)
    for inst,dist in generate_instructions("day12.dat"):
        if inst in "NSEW":
            ship.project(COMPASS[inst], dist)
        elif inst in "LR":
            heading.pivot(dist, 1 if inst == "R" else -1)
        elif inst in "F":
            ship.project(heading, dist)
    return ship.manhattan_distance(0, 0)

def parttwo():
    ship, wp = Vector(0, 0), Vector(10, -1)
    for inst, dist in generate_instructions("day12.dat"):
        if inst == "F":
            ship.project(wp, dist)
        elif inst in "LR":
            wp.pivot(dist, 1 if inst == "R" else -1)
        elif inst in "NSEW":
            wp.project(COMPASS[inst], dist)
    return ship.manhattan_distance(0, 0)

print(partone())
print(parttwo())
