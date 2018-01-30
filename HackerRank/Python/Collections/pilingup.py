from collections import deque

def sayit(seq):
    response = "Yes"
    while len(seq) and response == "Yes":
        max_pos = seq.index(max(seq))
        if max_pos == 0:
            seq.popleft()
        elif max_pos == len(seq)-1:
            seq.pop()
        else:
            response = "No"
    return response

if __name__ == "__main__":
    for tc in range(int(input())):
        s = int(input())
        row_of_cubes = deque(map(int, input().split()))
        response = sayit(row_of_cubes)
        print(response)