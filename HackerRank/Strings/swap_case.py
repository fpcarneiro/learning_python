def swap_case(s):
    x = ""
    for c in s:
        x = x + (c.upper() if c.islower() else c.lower())
    return x

print(swap_case("Www.HackerRank.com"))
