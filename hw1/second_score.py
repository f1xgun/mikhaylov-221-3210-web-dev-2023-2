n = int(input())
A = [int(x) for x in input().split()]
max_1 = max(A)
max_2 = -1
for i in range(len(A)):
    if A[i] != max_1:
        max_2 = max(max_2, A[i])
if max_2 == -1:
    print('Not found second place')
else:
    print(max_2)
