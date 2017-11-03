def merge_the_tools(string, k):
    # your code goes here
    for seg in get_string_segment(string, k):
        s = ""
        for c in seg:
            if c not in s:
                s += c
        print (s)


def get_string_segment(string, k):
    for i in range(0, len(string), k):
        yield (string[i:i+k])


if __name__ == '__main__':
#    string, k = input(), int(input())
    string = "AABCAAADA"
    k = 3
    merge_the_tools(string, k)