from itertools import product

A = [int(e) for e in input().split(" ")]
B = list(map(int, input().split(" ")))
A.sort()
B.sort()
PC = list(product(A, B))
PC.sort()
for i in PC:
    print i
