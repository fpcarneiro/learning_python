import numpy as np

[n, m, p] = [int(e) for e in input().split()]
a1 = np.array([[int(e) for e in input().split()] for i in range(n)])
a2 = np.array([[int(e) for e in input().split()] for i in range(m)])

print(np.concatenate((a1, a2), axis=0))
