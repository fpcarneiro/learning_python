from itertools import groupby

s = input()
l = [(len(list(i)), int(e)) for e,i in groupby(s)]
for e in l:
    print(e, end=" ")