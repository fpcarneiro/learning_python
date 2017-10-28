from operator import itemgetter

if __name__ == '__main__':
    students = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        students.append([name, score])
    students.sort(key=itemgetter(1, 0))

    grades = []
    [grades.append(g) for (s, g) in students if g not in grades]
    [print(s) for (s, g) in students if g == grades[1]]

