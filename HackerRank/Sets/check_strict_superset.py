A = set(input().split(" "))
n = int(input())
ss = True
for i in range(n):
    s = set(input().split(" "))
    ss = ss and A.issuperset(s)
    if ss == False:
        break
print(ss)