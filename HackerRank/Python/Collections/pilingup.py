from collections import deque
import re

def sayit(seq):
    response = True
    while (len(seq) >= 1) and response:
        max, seq, response = sayit2(seq)
    return (len(seq) <= 1)
    
def sayit2(seq):
    d = deque(map(int, seq.split()))
    max_number = max(d)
    
    pattern_ini = r'^(' + str(max_number) + '\s)' + '+'
    pattern_end = r'(\s' + str(max_number) + ')' + '+' + '$'
    p_ini = re.compile(pattern_ini)
    p_end = re.compile(pattern_end)
        
    seq, i = p_ini.subn( '', seq)
    seq, e = p_end.subn( '', seq)
    
    d = deque(map(int, seq.split()))
    max_count = d.count(max_number)
    
    response = (max_count == 0)
    
    return max_number, seq, response

if __name__ == "__main__":
    rows_of_cubes = []
    for tc in range(int(input())):
        s = int(input())
        rows_of_cubes.append(input())
    for e in rows_of_cubes:
        response = sayit(e)
        if response:
            print("Yes")
        else:
            print("No")
