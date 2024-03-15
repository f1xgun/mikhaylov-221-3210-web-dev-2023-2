n = int(input())
a = []
b = []
for i in range(n):
    a.append(list(map(int, input().split())))

for i in range(n):
    b.append(list(map(int, input().split())))

c = [[0] * n for i in range(n)]

for i in range(n):
    for j in range(n):
        for k in range(n):
            c[i][j] += a[i][k] * b[k][j]

for i in range(n):
    print(*c[i])
