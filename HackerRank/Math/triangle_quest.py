for i in range(1, int(input()) + 1):
    print(sum(map((lambda x, y: x*y), (map((lambda x: 10**x), (range(i-1, -1, -1)))), ([i] * i))))
