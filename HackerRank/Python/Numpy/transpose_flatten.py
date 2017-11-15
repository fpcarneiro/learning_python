import numpy as np

[lines, columns] = [int(e) for e in input().split()]
m = np.array([[int(e) for e in input().split()] for i in range(lines)])
print(m.transpose())
print(m.flatten())
