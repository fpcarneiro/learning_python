from collections import OrderedDict

items_dictionary = OrderedDict()
N = int(input())
for prod in range(N):
    tmp = input().rpartition(" ")
    items_dictionary[tmp[0]] = items_dictionary.get(tmp[0], 0) + int(tmp[2])

for prod in items_dictionary.items():
    print("%s %s" % prod)