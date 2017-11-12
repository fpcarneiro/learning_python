if __name__ == "__main__":
    n, m = map(int, input("Choose N and M, please: ").split(" "))
    array = [int(e) for e in input("Enter your %s elements: " % n).split(" ")]
    A = {int(e) for e in input("Enter your %s elements for A: " % m).split(" ")}
    B = {int(e) for e in input("Enter your %s elements for B: " % m).split(" ")}
    hapiness = 0
    for e in array:
        if e in A:
            hapiness += 1
        elif e in B:
            hapiness += -1

    print(hapiness)
