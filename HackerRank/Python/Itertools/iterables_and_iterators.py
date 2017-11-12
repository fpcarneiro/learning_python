from itertools import combinations

def find_indexes(elem, list):
    return [idx+1 for (idx, el) in enumerate(list) if elem == el]

n = int(input())
s = input().split(" ")

c = list(combinations(range(1,n+1), int(input())))
co = set()
for i in find_indexes('a', s):
    co.update(set(filter(lambda x: i in x, c)))
print("%.4f" % (len(co)/len(c)))