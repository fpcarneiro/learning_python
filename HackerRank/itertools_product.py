from itertools import product
A = [int(e) for e in input().split(" ")]
B = list(map(int, input().split(" ")))
A.sort()
B.sort()
C = list(product(A, B))
C.sort()
for e in C:
    print(e, end=" ")