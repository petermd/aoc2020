import re

def generate_records(file):
    cur = {}
    pattern = re.compile("(\w+):(.+)")
    with open(file, "r") as f:
        for line in [l.rstrip() for l in f.readlines()]:
            if line == "":
                yield cur
                cur = {}
            for m in [ pattern.match(a) for a in line.split() ]:
                cur[m[1]] = m[2]
    yield cur

MANDATORY = ["byr","iyr","eyr","hgt","hcl","ecl","pid"]

def valid(record):
    for f in MANDATORY:
        if f not in record:
            return False
    return True

def partone():
    num_valid = 0
    for r in generate_records("day4.dat"):
        if valid(r):
            num_valid += 1
    return num_valid

def valid_year(year):
    return int(year)

def strict_valid(record):

    if not valid(record):
        raise Exception("missing fields")

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if 1920 <= valid_year(record["byr"]) <= 2002:
        pass
    else:
        raise Exception("invalid byr", valid_year(record["byr"]))

    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if 2010 <= valid_year(record["iyr"]) <= 2020:
        pass
    else:
        raise Exception("invalid iyr", valid_year(record["iyr"]))

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if 2020 <= valid_year(record["eyr"]) <= 2030:
        pass
    else:
        raise Exception("invalid eyr", valid_year(record["eyr"]))

    # hgt (Height) - a number followed by either cm or in:
    # If cm, the number must be at least 150 and at most 193.
    # If in, the number must be at least 59 and at most 76.
    mh = re.fullmatch("(\d*)(cm|in)", record["hgt"])
    if mh:
        if mh[2] == "cm" and 150 <= int(mh[1]) <= 193:
            pass
        elif mh[2] == "in" and 59 <= int(mh[1]) <= 76:
            pass
        else:
            raise Exception("invalid hgt", record["hgt"])
    else:
        raise Exception("invalid hgt format", record["hgt"])

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    mhcl = re.fullmatch("#([0-9a-f]{6})", record["hcl"])
    if mhcl:
        pass
    else:
        raise Exception("invalid hcl", record["hcl"])

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if record["ecl"] not in ["amb","blu","brn","gry","grn","hzl","oth"]:
        raise Exception("invalid ecl", record["ecl"])

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    mpid = re.fullmatch("(\d{9})", record["pid"])
    if not mpid:
        raise Exception("invalid pid", record["pid"])

    # cid (Country ID) - ignored, missing or not.

def parttwo():
    total, num_valid = 0, 0
    for r in generate_records("day4.dat"):
        total += 1
        try:
            strict_valid(r)
            num_valid += 1
        except Exception as ex:
            print(ex)
    return num_valid, total

print(parttwo())
