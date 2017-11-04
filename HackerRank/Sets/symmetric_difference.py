if __name__ == "__main__":
    m = int(input())
    sm = set(map(int, input().split()))
    n = int(input())
    sn = set(map(int, input().split()))
    result = sm ^ sn
    for e in sorted(result):
        print(e)