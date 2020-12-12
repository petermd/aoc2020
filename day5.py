def locate(left, right, key):
    for c in key:
        if c in ["F", "L"]:
            right = left + (right - left + 1) // 2 - 1
        elif c in ["B", "R"]:
            left = left + (right - left + 1) // 2
    return left

def seat(key):
    row = locate(0, 127, key[:7])
    seat = locate(0, 7, key[7:])
    return row, seat, row * 8 + seat

def partone():
    max_id = 0
    with open("day5.dat", "r") as f:
        for bc in [l.rstrip() for l in f.readlines()]:
            r, s, id = seat(bc)
            max_id = max(id, max_id)
    return max_id

def parttwo():
    max_id = 0
    full = [0] * 1024
    with open("day5.dat", "r") as f:
        for bc in [l.rstrip() for l in f.readlines()]:
            r, s, id = seat(bc)
            max_id = max(id, max_id)
            full[id] = 1

    for idx in range(1, max_id - 1):
        if not full[idx] and full[idx - 1] and full[idx + 1]:
            return idx

print(parttwo())
