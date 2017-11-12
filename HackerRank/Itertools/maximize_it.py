from itertools import product

values = [int(v) for v in input().split()]
k, m = values[0], values[1]
lists_squared = [list(map((lambda x: x ** 2), map(int, (input().split()[1:])))) for i in range(k)]
l = list(product(*lists_squared))
print(max(list(map(lambda x: sum(x) % m, l))))
