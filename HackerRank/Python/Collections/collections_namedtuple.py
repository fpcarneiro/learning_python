from collections import namedtuple

N = int(input())
columns = input().split()
Student = namedtuple('Student', columns)

the_class = [Student._make(input().split()) for s in range(N)]

soma = 0
for e in the_class:
    soma += int(e.MARKS)
print("%.2f" % (soma / N))
