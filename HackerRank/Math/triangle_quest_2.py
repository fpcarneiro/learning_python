for i in range(1, int(input())+1): #More than 2 lines will result in 0 score. Do not leave a blank line also
    print(sum(map((lambda x, y: x*y), (map((lambda x: 10**x), (range((2*i)-2, -1, -1)))), (list(range(1, i+1)) + list(range(i-1, 0, -1))))))