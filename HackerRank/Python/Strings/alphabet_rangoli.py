def print_rangoli(size):
    alphabet = 'abcdefghijklmnoqrstuvwxyz'
    c = "-".join(alphabet[size-1::-1] + alphabet[1:size])
    for i in range(size-1, 0, -1):
        front = alphabet[size-1:i:-1]
        back = alphabet[i:size]
        print("-".join(front + back).center(len(c), "-"))
    print(c)
    for i in range(1, size):
        front = alphabet[size-1:i:-1]
        back = alphabet[i:size]
        print("-".join(front + back).center(len(c), "-"))
