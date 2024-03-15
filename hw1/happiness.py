n, m = map(int, input().split())
arr = list(map(int, input().split()))
a = set(map(int, input().split()))
b = set(map(int, input().split()))

happiness = 0
for el in arr:
    if el in a:
        happiness += 1
    elif el in b:
        happiness -= 1

print(happiness)
