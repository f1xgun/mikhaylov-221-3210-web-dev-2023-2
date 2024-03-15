def average_scores(grades: list[tuple[float, ...]]) -> tuple[float, ...]:
    if len(grades) == 0:
        return tuple()
    result = [0.0] * len(grades[0])
    for subject in grades:
        for student_ind in range(len(subject)):
            result[student_ind] += subject[student_ind]
    return tuple(map(lambda a: a / len(grades), result))


if __name__ == "__main__":
    n, x = map(int, input().split())
    grades_input = [tuple(map(float, input().split())) for i in range(x)]
    print('\n'.join(map(str, average_scores(grades_input))))
