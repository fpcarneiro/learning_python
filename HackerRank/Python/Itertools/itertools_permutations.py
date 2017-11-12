from itertools import permutations

s_k = input().split(" ")
per = list(permutations(s_k[0], int(s_k[1])))
per.sort()
for e in per:
    print("".join(e))
