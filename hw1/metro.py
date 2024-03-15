n = int(input())
intervals = []
for i in range(n):
    a, b = map(int, input().split())
    intervals.append([a, b])

t = int(input())
count = 0
for interval in intervals:
    if interval[0] <= t <= interval[1]:
        count += 1

print(count)
