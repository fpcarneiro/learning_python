def count_substring(string, sub_string):
    count = 0
    pos = string.find(sub_string)
    while pos != -1:
        count += 1
        string = string[pos+1:]
        pos = string.find(sub_string)
    return count

#print(count_substring("ABCDCDC", "CDC"))
