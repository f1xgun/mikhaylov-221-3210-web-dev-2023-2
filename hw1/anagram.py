from collections import defaultdict

str1 = input().strip()
str2 = input().strip()

if len(str1) != len(str2):
    print("NO")
else:
    d = defaultdict(int)
    for i in range(len(str1)):
        d[str1[i]] += 1
        d[str2[i]] -= 1

    if len(set(d.values())) != 1:
        print("NO")
    else:
        print("YES")
