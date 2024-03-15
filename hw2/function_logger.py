import functools
from datetime import datetime


def function_logger(filepath: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            with open(filepath, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Название функции: {func.__name__},\n")
                log_file.write(f"Время вызова функции: {start_time.strftime('%Y-%m-%d %H:%M:%S')},\n")
                log_file.write(f"Входящие аргументы: позиционные - {args}, ключевые - {kwargs},\n")
                log_file.write(f"Возвращаемое значение: {result if result is not None else '-'},\n")
                log_file.write(f"Время завершения работы функции: {end_time.strftime('%Y-%m-%d %H:%M:%S')},\n")
                log_file.write(f"Время работы функции: {duration} секунд.\n\n")

            return result
        return wrapper
    return decorator


@function_logger('function_log.txt')
def test_function(a: int, b: int = 10):
    return a + b


@function_logger('function_log.txt')
def fibonacci(n: int):
    if n == 1:
        return [0]
    result = [0, 1]
    for i in range(2, n):
        result.append(result[i - 2] + result[i - 1])
    return result


if __name__ == '__main__':
    test_function(5)
    test_function(15, b=20)
    fibonacci(10)
