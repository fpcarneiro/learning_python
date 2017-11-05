commands = {"pop": set.pop, "discard": set.discard, "remove": set.remove}

if __name__ == "__main__":
    n = int(input())
    s = {int(e) for e in input().split(" ")}
    N = int(input())
    for c in range(N):
        co = input().split(" ")
        f = commands[co[0]]
        if co[0] != "pop":
            f(s,int(co[1]))
        else:
            f(s)
    print(sum(s))