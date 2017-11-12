from itertools import product

[k, m] = [int(v) for v in input().split()]
lists_squared = [list(map((lambda x: x ** 2), map(int, (input().split()[1:])))) for i in range(k)]
l = list(product(*lists_squared))
print(max(list(map(lambda x: sum(x) % m, l))))
