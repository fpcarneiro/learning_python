values = [int(v) for v in input().split()]
k, m = values[0], values[1]
lists = [list(map(int, (input().split())))[1:] for i in range(k)]
print(lists)