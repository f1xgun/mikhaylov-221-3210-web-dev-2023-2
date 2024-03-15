cube = lambda x: x ** 3  # complete the lambda function


def fibonacci(n: int):
    if n == 1:
        return [0]
    result = [0, 1]
    for i in range(2, n):
        result.append(result[i - 2] + result[i - 1])
    return list(map(cube, result))


if __name__ == '__main__':
    num = int(input())
    print(fibonacci(num))
