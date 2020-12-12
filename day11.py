from copy import deepcopy

floor=[]
with open("day11.dat") as f:
    for rs in f.readlines():
        floor.append(list(rs.rstrip()))

width = len(floor[0])
height = len(floor)

DIRECTIONS = [
    (-1,-1),(0,-1),(+1,-1),
    (-1,0),        (+1,0),
    (-1,+1),(0,+1),(+1,+1)
]

def valid(x, y):
    return False if (x < 0 or x >= width or y < 0 or y >= height) else True

def occupied(x, y):
    return valid(x, y) and floor[y][x] == '#'

def count_neighbours(x,y):
    return sum([occupied(x + ix,y + iy) for (ix, iy) in DIRECTIONS])

def count_visible(x,y):
    total = 0
    for (ix, iy) in DIRECTIONS:
        cx, cy = x, y
        while(valid(cx + ix, cy + iy)):
            cx += ix
            cy += iy
            if floor[cy][cx] == '.':
                continue
            total += occupied(cx, cy)
            break
    return total

def count_occupied():
    total = 0
    for iy in range(height):
        for ix in range(width):
            total += floor[iy][ix] == '#'
    return total

def dump():
    for y in range(height):
        print("".join(floor[y]))

def refresh(check_fn, limit):
    global floor

    update = deepcopy(floor)
    updates = 0
    for iy in range(height):
        for ix in range(width):
            change = None
            if floor[iy][ix] == '.':
                continue
            elif floor[iy][ix] == 'L' and check_fn(ix, iy) == 0:
                change = '#'
            elif floor[iy][ix] == '#' and check_fn(ix, iy) >= limit:
                change = 'L'
            else:
                continue

            updates += 1
            update[iy][ix] = change

    floor = update

    return updates

def partone():
    iterations = 0
    while refresh(count_neighbours, 4) > 0:
        iterations += 1

    print("stable after", iterations)
    dump()

    return count_occupied()

def parttwo():
    iterations = 0
    while refresh(count_visible, 5) > 0:
        iterations += 1

    print("stable after", iterations)
    dump()

    return count_occupied()

print(parttwo())
