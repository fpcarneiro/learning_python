from itertools import combinations_with_replacement

s_k = input().split(" ")
l = list(s_k[0])
l.sort()
for e in combinations_with_replacement(l, int(s_k[1])):
    print("".join(e))
