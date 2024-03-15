n = int(input())
arr = []


def parse_command(command, args):
    if command == 'insert':
        if len(args) != 2:
            print('Error INSERT command need 2 arguments')
            return
        first = int(args[0])
        second = int(args[1])
        arr.insert(first, second)
    elif command == 'print':
        if len(arr) == 0:
            print('No element in list')
        else:
            print(*arr)
    elif command == 'remove':
        if len(args) != 1:
            print('Error REMOVE command need one argument')
            return
        if int(args[0]) in arr:
            arr.remove(int(args[0]))
    elif command == 'append':
        if len(args) != 1:
            print('Error APPEND command need one argument')
            return
        arr.append(int(args[0]))
    elif command == 'sort':
        arr.sort()
    elif command == 'pop':
        arr.pop()
    elif command == 'reverse':
        arr.reverse()


for i in range(n):
    input_str = input().strip().split()
    command = input_str[0]
    parse_command(command, input_str[1:])

