import numpy as np

n, m = tuple(map(int, input().split()))
A = np.array([list(map(int, input().split())) for i in range(n)], int)
B = np.array([list(map(int, input().split())) for i in range(n)], int)
print(np.add(A, B))
print(np.subtract(A, B))
print(np.multiply(A, B))
print(np.floor_divide(A, B))
print(np.mod(A, B))
print(np.power(A, B))

