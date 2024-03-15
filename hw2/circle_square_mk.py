import math
import random


def circle_square_mk(r: float, n: int) -> float:
    i = 0
    count = 0
    while i < n:
        x = random.random()
        y = random.random()
        if (pow(x, 2) + pow(y, 2)) < 1:
            count += 1
        i += 1
    return 4 * (count / n) * pow(r, 2)


if __name__ == '__main__':
    r, n = map(float, input().split())
    for i in range(20):
        print(circle_square_mk(r, n))
    print(math.pi * pow(r, 2))
    # n == 10: 2.7 - 3.6 14%
    # n == 100: 2.88 - 3.28 8%
    # n == 1000: 3.044 - 3.204 3%
    # n == 10000: 3.118 - 3.1684 0.7%
    # n == 100000: 3.12972 - 3.14788 0.37%
