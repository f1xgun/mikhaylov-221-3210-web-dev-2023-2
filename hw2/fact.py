import sys
import time


def fact_rec(number):
    if number == 1:
        return 1
    return fact_rec(number - 1) * number


def fact_it(number):
    result = 1
    for i in range(2, number + 1):
        result *= i
    return result


if __name__ == '__main__':
    sys.setrecursionlimit(10001)
    start_time_rec = time.time()
    print(start_time_rec)
    fact_rec(2670)
    end_time_rec = time.time()
    print(end_time_rec)
    start_time_it = time.time()
    fact_it(2670)
    end_time_it = time.time()
    print(
        f"Recursion time: {format(end_time_rec - start_time_rec, '.4f')} sec and"
        f" iteration time: {format(end_time_it - start_time_it, '.4f')} sec")
    # Recursion time: 0.0040 sec and iteration time: 0.0015 sec
