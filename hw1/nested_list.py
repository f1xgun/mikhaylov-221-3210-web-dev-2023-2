n = int(input())
records = []
for i in range(n):
    name = input()
    grade = float(input())
    records.append([name, grade])

second_place_students = []
min_grade = min([record[1] for record in records])
second_place_grade = float('inf')
for i in range(n):
    if records[i][1] != min_grade:
        if records[i][1] < second_place_grade:
            second_place_grade = records[i][1]
            second_place_students = [records[i][0]]
        elif records[i][1] == second_place_grade:
            second_place_students.append(records[i][0])

if len(second_place_students) == 0:
    print('Not found students with second place grade')
else:
    print('\n'.join(sorted(second_place_students)))
