import subprocess
import pytest

from average_scores import average_scores
from complex_numbers import Complex, run_operations
from email_validation import filter_mail
from fact import fact_it, fact_rec
from fibonacci import fibonacci
from file_search import file_search
from files_sort import files_sort
from my_sum import my_sum
from people_sort import name_format
from phone_number import sort_phone
from plane_angle import plane_angle, Point
from process_list import process_list, process_list_gen
from show_employee import *
from sum_and_sub import sum_and_sub

INTERPRETER = 'python3'


def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()


test_data = {
    'fact': [
        (5, 120),
        (1, 1),
        (100,
         93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000)
    ],
    'show_employee': [
        (['Иванов Иван Иванович', '151123'], 'Иванов Иван Иванович: 151123 ₽'),
        (['Иванов Иван Иванович'], 'Иванов Иван Иванович: 10000 ₽'),
        (['Иван'], 'Иван: 10000 ₽')
    ],
    'sum_and_sub': [
        ([1, 2], [3, -1]),
        ([0, 0], [0, 0]),
        ([5, -3], [2, 8]),
        ([-1.2, -5.3], [-6.5, 4.1])
    ],
    'process_list': [
        ([1], [1]),
        ([1, 3, -2], [1, 27, 4]),
        ([0, -5, -20], [0, -125, 400]),
    ],
    'my_sum': [
        ([], 0),
        ([1.0, -2.5], -1.5),
        ([1.3, 2.6, 1.0, 1.27], 6.17),
        ([-5.0, -5.9], -10.9)
    ],
    'files_sort': [
        ('./files_sort_test_dir/', ['b.py', 'c.py', 'a.txt', 'b.txt', 'c.txt'])
    ],
    'file_search': [
        ('a.txt', '\n'.join(['Э', 'т', 'о', 'ф', 'а'])),
        ('b.py', '\n'.join(["print('Hello world')"])),
        ('not_found.txt', 'Файл not_found.txt не найден'),
        ('test.py', '\n'.join(['import subprocess', 'import pytest', '', 'from average_scores import average_scores',
                               'from complex_numbers import Complex, run_operations']))
    ],
    'email_validation': [
        (['brian-23@mospolytech.ru', 'britts_54@mospolytech.ru', 'lara@mospolytech.ru'],
         ['brian-23@mospolytech.ru', 'britts_54@mospolytech.ru', 'lara@mospolytech.ru']),
        (['asd_1!3@mospolytech.ru', 'brian-23@mospolytech.ru'], ['brian-23@mospolytech.ru']),
        (['brian-23@mospolytech.russia'], []),
        (['brian-23@mospolytech.r1u'], []),
        (['brian-23@mospolyt_ech.ru'], []),
        (['brian-23@mospolytech..ru'], []),
        (['bri@an-23@mospolytech.ru'], [])
    ],
    'fibonacci': [
        (1, [0]),
        (2, [0, 1]),
        (4, [0, 1, 1, 8]),
        (10, [0, 1, 1, 8, 27, 125, 512, 2197, 9261, 39304])
    ],
    'average_scores': [
        ([[75]], (75.0,)),
        ([[70, 85, 90]], (70.0, 85.0, 90.0)),
        ([[90.5], [89.5], [90]], (90,)),
        ([[89, 90, 78, 93, 80], [90, 91, 85, 88, 86], [91, 92, 83, 89, 90.5]], (90.0, 91.0, 82.0, 90.0, 85.5))
    ],
    'phone_number': [
        (['07895462130'], ['+7 (789) 546-21-30']),
        (['89875641230'], ['+7 (987) 564-12-30']),
        (['9195969878'], ['+7 (919) 596-98-78']),
        (['+79051235482'], ['+7 (905) 123-54-82']),
        (['07895462130', '89875641230', '9195969878', '+79051235482'],
         ['+7 (789) 546-21-30', '+7 (905) 123-54-82', '+7 (919) 596-98-78', '+7 (987) 564-12-30'])
    ],
    'people_sort': [
        ([['Mike', 'Thomson', '20', 'M'], ['Robert', 'Bustle', '32', 'M'], ['Andria', 'Bustle', '30', 'F']],
         ['Mr. Mike Thomson', 'Ms. Andria Bustle', 'Mr. Robert Bustle']),
        ([['Robert', 'Bustle', '32', 'M'], ['Andria', 'Bustle', '30', 'F'], ['Mike', 'Thomson', '20', 'M']],
         ['Mr. Mike Thomson', 'Ms. Andria Bustle', 'Mr. Robert Bustle']),
        ([['Robert', 'Bustle', '32', 'F'], ['Andria', 'Bustle', '30', 'F'], ['Mike', 'Thomson', '20', 'F']],
         ['Ms. Mike Thomson', 'Ms. Andria Bustle', 'Ms. Robert Bustle']),
        ([['Robert', 'Bustle', '32', 'M'], ['Andria', 'Bustle', '30', 'F'], ['Mike', 'Thomson', '30', 'M']],
         ['Ms. Andria Bustle', 'Mr. Mike Thomson', 'Mr. Robert Bustle'])
    ],
    'plane_angle': [
        ([[1, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0]], 45.0),
        ([[2, 3, 1], [0, 1, 0], [1, 2, 0], [1, 0, 0]], 90.0),
        ([[2, 0, 1], [0, 1, 2], [1, 2, 3], [1, 1, 2]], 0.0),
        ([[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1]], 35.26),
        ([[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 2, 1]], 70.53)
    ],
    'complex_numbers': [
        ([[2, 1], [5, 6]], ['7.00+7.00i', '-3.00-5.00i', '4.00+17.00i', '0.26-0.11i', '2.24+0.00i', '7.81+0.00i']),
        ([[3, 0], [5, 0]], ['8.00+0.00i', '-2.00+0.00i', '15.00+0.00i', '0.60+0.00i', '3.00+0.00i', '5.00+0.00i']),
        ([[0, 1], [0, -6]], ['0.00-5.00i', '0.00+7.00i', '6.00+0.00i', '-0.17+0.00i', '1.00+0.00i', '6.00+0.00i']),
    ]
}


@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_it(input_data, expected):
    assert fact_it(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['fact'])
def test_fact_rec(input_data, expected):
    assert fact_rec(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['show_employee'])
def test_show_employee(input_data, expected):
    assert show_employee(*input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['sum_and_sub'])
def test_sum_and_sub(input_data, expected):
    assert sum_and_sub(*input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['process_list'])
def test_process_list(input_data, expected):
    assert process_list(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['process_list'])
def test_process_list_gen(input_data, expected):
    assert process_list_gen(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['my_sum'])
def test_my_sum(input_data, expected):
    assert my_sum(*input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['files_sort'])
def test_files_sort(input_data, expected):
    assert files_sort(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['file_search'])
def test_file_search(input_data, expected):
    assert file_search(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['email_validation'])
def test_email_validation(input_data, expected):
    assert filter_mail(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['fibonacci'])
def test_fibonacci(input_data, expected):
    assert fibonacci(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['average_scores'])
def test_average_scores(input_data, expected):
    assert average_scores(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['phone_number'])
def test_phone_number(input_data, expected):
    assert sort_phone(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['people_sort'])
def test_people_sort(input_data, expected):
    assert name_format(input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['plane_angle'])
def test_plane_angle(input_data, expected):
    data = [Point(*map(float, input)) for input in input_data]
    assert plane_angle(*data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['complex_numbers'])
def test_complex_numbers(input_data, expected):
    data = [Complex(*map(float, input)) for input in input_data]
    assert run_operations(*data) == expected
