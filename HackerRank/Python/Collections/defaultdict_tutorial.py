from collections import defaultdict
A = defaultdict(list)
B = defaultdict(list)

m, n = list(map(int, input().split()))
for i in range(m):
    A[input()].append(i+1)
for i in range(n):
    B[input()].append(i + 1)

for e in B.keys():
    for el in A.get(e, [-1]):
        print(el, end=" ")
    print()