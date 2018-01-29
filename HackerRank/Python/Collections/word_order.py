from collections import OrderedDict

words_dictionary = OrderedDict()
N = int(input())
for w in range(N):
    word = input()
    words_dictionary[word] = words_dictionary.get(word, 0) + 1

print(len(words_dictionary))
for s in list(words_dictionary.values()):
    print(s, end= " ")