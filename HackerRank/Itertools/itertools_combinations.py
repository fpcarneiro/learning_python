from itertools import combinations

s_k = input().split(" ")
l = list(s_k[0])
l.sort()
for i in range(1, int(s_k[1]) + 1):
    comb = list(combinations(l, i))
    comb.sort()
    for e in comb:
        print("".join(e))
