import time


def process_list(arr: list[int]) -> list[int]:
    result = []
    for i in arr:
        if i % 2 == 0:
            result.append(i ** 2)
        else:
            result.append(i ** 3)
    return result


def process_list_gen(arr: list[int]) -> list[int]:
    return [i ** 2 if i % 2 == 0 else i ** 3 for i in arr]


if __name__ == '__main__':
    example_arr: list[int] = [i for i in range(1000000)]
    start_time = time.time()
    process_list(example_arr)
    end_time = time.time()
    start_time_gen = time.time()
    process_list_gen(example_arr)
    end_time_gen = time.time()
    print(
        f"Example time: {format(end_time - start_time, '.4f')} sec\n"
        f"Gen time: {format(end_time_gen - start_time_gen, '.4f')} sec")
    # Example time: 0.2762 sec
    # Gen time: 0.2614 sec
