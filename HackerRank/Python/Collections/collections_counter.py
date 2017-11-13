from collections import Counter

X = int(input())
shoe_sizes = Counter(list(map(int, input().split())))
N = int(input())
amount = 0
for i in range(N):
    size, price = tuple(map(int, input().split()))
    if shoe_sizes.get(size, 0) > 0:
        shoe_sizes[size] -= 1
        amount += price
print(amount)
