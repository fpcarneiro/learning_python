operations = {"intersection_update": set.intersection_update, "update": set.update, "symmetric_difference_update": set.symmetric_difference_update, "difference_update": set.difference_update}

n_a = int(input())
A = set(map(int, input().split(" ")))
N = int(input())
for operation in range(N):
    oper, length = input().split(" ")
    operations[oper](A, set(map(int, input().split(" "))))
print(sum(A))