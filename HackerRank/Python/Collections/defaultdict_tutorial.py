from collections import defaultdict
A = defaultdict(list)

m, n = list(map(int, input().split()))
for i in range(m):
    A[input()].append(i+1)
B = [input() for i in range(n)]

for e in B:
    print(" ".join(map(str, A.get(e, [-1]))))