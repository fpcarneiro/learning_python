X = int(input())
shoe_sizes = list(map(int, input().split()))
N = int(input())
customers = []
for i in range(N):
    customers.append(tuple(map(int, input().split())))
print(customers)
