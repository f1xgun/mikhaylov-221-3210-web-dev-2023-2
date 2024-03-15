import argparse


def my_sum(*args: tuple[any]) -> float:
    return sum(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('integers', nargs='*', type=int)
    arguments = parser.parse_args()
    print(my_sum(*arguments.integers))
