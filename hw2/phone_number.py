def wrapper(f):
    def fun(l):
        formatted_numbers = []
        for number in l:
            number_without_prefix: str = number[len(number) - 10:]
            formatted_number = f"+7 ({number_without_prefix[:3]}) {number_without_prefix[3:6]}-{number_without_prefix[6:8]}-{number_without_prefix[8:]}"
            formatted_numbers.append(formatted_number)
        return f(formatted_numbers)

    return fun


@wrapper
def sort_phone(l):
    return sorted(l)


if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
