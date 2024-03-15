import csv
import subprocess
import pytest
import shutil
import os

INTERPRETER = 'python3'


def change_list_elements_from_list_to_str(arr: list) -> list:
    if arr:
        for i in range(len(arr)):
            if type(arr[i]) is list:
                arr[i] = ' '.join(arr[i])
    return arr


def run_script(filename, input_data=None):
    input_data = change_list_elements_from_list_to_str(input_data)

    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()


test_data = {
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6', 'Weird'),
        ('22', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50']),
        (['-1', '3'], ['2', '-4', '-3']),
        (['2', '-5'], ['-3', '7', '-10']),
        (['-3', '-4'], ['-7', '1', '12'])
    ],
    'division': [
        (['4', '2'], ['2', '2.0']),
        (['5', '2'], ['2', '2.5']),
        (['2', '4'], ['0', '0.5']),
        (['-2', '4'], ['0', '-0.5']),
        (['4', '-2'], ['-2', '-2.0']),
        (['-2', '-4'], ['0', '0.5'])
    ],
    'loops': [
        ('1', ['0']),
        ('2', ['0', '1']),
        ('3', ['0', '1', '4']),
        ('5', ['0', '1', '4', '9', '16'])
    ],
    'print_function': [
        ('1', '1'),
        ('2', '12'),
        ('10', '12345678910'),
        ('20', '1234567891011121314151617181920')
    ],
    'second_score': [
        (['5', ['2', '3', '6', '6', '5']], '5'),
        (['2', ['1', '1']], 'Not found second place'),
        (['1', ['2']], 'Not found second place'),
        (['6', ['1', '2', '3', '4', '3', '2']], '3')
    ],
    'nested_list': [
        (['1', 'Иван', '10'], ['Not found students with second place grade']),
        (['2', 'Иван', '10', 'Иван', '10'], ['Not found students with second place grade']),
        (['3', 'Иван', '10', 'Дима', '9.9', 'Артем', '10'], ['Артем', 'Иван']),
        (['3', 'Иван', '10', 'Дима', '9.9', 'Артем', '11'], ['Иван']),
        (['5', 'Иван', '10', 'Дима', '9.9', 'Артем', '10', 'Семен', '10', 'Маша', '10'],
         ['Артем', 'Иван', 'Маша', 'Семен']),
    ],
    'lists': [
        (['4', ['insert', '0', '5'], 'print', ['pop'], 'print'], ['5', 'No element in list']),
        (['12', ['insert', '0', '5'], ['insert', '1', '10'], ['insert', '0', '6'], 'print', ['remove', '6'],
          ['append', '9'], ['append', '1'], 'sort', 'print', 'pop', 'reverse', 'print'],
         [['6', '5', '10'], ['1', '5', '9', '10'], ['9', '5', '1']]),
        (['4', ['append', '1'], ['append', '2'], ['insert', '1', '3'], 'print'], [['1', '3', '2']]),
        (['4', ['insert'], ['insert', '1'], ['remove'], ['append']],
         ['Error INSERT command need 2 arguments', 'Error INSERT command need 2 arguments',
          'Error REMOVE command need one argument', 'Error APPEND command need one argument'])
    ],
    'swap_case': [
        ('Www.MosPolytech.ru', 'wWW.mOSpOLYTECH.RU'),
        ('Pythonist 2', 'pYTHONIST 2'),
        ('!@#$%^^&*()_+asidzZXAS', '!@#$%^^&*()_+ASIDZzxas'),
        ('АбВгДеЁжЗиЙкЛмНоПрСтУфХцЧшЩъЫьЭюЯ', 'аБвГдЕёЖзИйКлМнОпРсТуФхЦчШщЪыЬэЮя')
    ],
    'split_and_join': [
        ('@a zgfdk  asd213', '@a-zgfdk-asd213'),
        ('  asdas  qwnejkqwne   ', 'asdas-qwnejkqwne')
    ],
    'anagram': [
        (['asdasd', 'dsadsa'], 'YES'),
        (['asdnjs', 'asdnja'], 'NO'),
        (['ASDasd', 'ASdasd'], 'NO'),
        (['asjdnasd', 'asd'], 'NO')
    ],
    'metro': [
        (['4', ['3', '5'], ['2', '3'], ['2', '4'], ['5', '7'], '3'], '3'),
        (['0', '0'], '0'),
        (['2', ['2', '4'], ['3', '6'], '1'], '0')
    ],
    'minion_game': [
        ('BANANA', [['STUART', '12']]),
        ('A', [['KEVIN', '1']]),
        ('MILK', [['STUART', '7']]),
        ('ABC', [['NOBODY WIN']])
    ],
    'is_leap': [
        ('2000', 'True'),
        ('1900', 'False'),
        ('2016', 'True'),
        ('2400', 'True'),
        ('2002', 'False'),
        ('2003', 'False'),
        ('2001', 'False'),
        ('2100', 'False')
    ],
    'happiness': [
        ([['3', '2'], ['1', '5', '3'], ['3', '1'], ['5', '7']], '1'),
        ([['0', '0'], '', '', '', ''], '0'),
        ([['3', '2'], ['1', '1', '1'], ['1', '2'], ['3', '4']], '3')
    ],
    'pirate_ship': [
        ([['15', '4'], ['Шкура', '8', '12'], ['Жемчужины', '6', '10'], ['Ром', '4', '8'], ['Сундук', '10', '15']],
         [['Жемчужины', '6.0', '10.0'], ['Ром', '4.0', '8.0'], ['Шкура', '5.0', '7.5']]),
        ([['20', '2'], ['Коробка', '10', '18'], ['Свиток', '5', '8'], ['Ром', '4', '8'], ['Сундук', '10', '15']],
         [['Коробка', '10.0', '18.0'], ['Свиток', '5.0', '8.0']]),
        ([['8', '4'], ['Лекарство', '2', '5'], ['Карта', '3', '6'], ['Свиток', '1', '3'], ['Зелье', '4', '7']],
         [['Карта', '3.0', '6.0'], ['Лекарство', '2.0', '5.0'],
          ['Зелье', '2.0', '3.5'], ['Свиток', '1.0', '3.0']])
    ],
    'matrix_mult': [
        (['2', ['2', '-6'], ['-6', '21'], ['7', '3'], ['2', '1']], [['2', '0'], ['0', '3']]),
        (['2', ['4', '3'], ['7', '5'], ['-28', '93'], ['38', '-126']], [['2', '-6'], ['-6', '21']]),
        (['5', ['1', '0', '4', '0', '0'], ['0', '7', '9', '1', '2'], ['0', '2', '3', '0', '4'],
          ['5', '7', '1', '2', '2'], ['3', '4', '3', '7', '2'], ['9', '3', '1', '5', '3'], ['4', '5', '8', '9', '2'],
          ['5', '3', '5', '3', '0'], ['0', '5', '4', '0', '2'], ['6', '7', '0', '8', '1']],
         [['29', '15', '21', '17', '3'], ['85', '81', '105', '106', '18'], ['47', '47', '31', '59', '8'],
          ['90', '77', '74', '107', '35'], ['70', '87', '78', '76', '33']]),
        (
            ['3', ['2', '1', '1'], ['1', '1', '1'], ['1', '1', '2'], ['1', '-1', '0'], ['-1', '3', '-1'],
             ['0', '-1', '1']],
            [['1', '0', '0'], ['0', '1', '0'], ['0', '0', '1']])
    ],
    'max_word': [
        ('', ['']),
        ('Самое большое слово здесь это кодирование', ['кодирование']),
        ('Молоко дорога машина', ['Молоко', "дорога", "машина"])
    ],
    'price_sum': [
        ([['Продукт', 'Взрослый', 'Пенсионер', 'Ребенок'], ['говядина', '909.0', '105.3', '1237.4'],
          ['капуста', '504.12', '483.2', '132.6']], ['1413.12', '588.50', '1370.00']),
        ([['Продукт', 'Взрослый', 'Пенсионер', 'Ребенок']], ['0.00', '0.00', '0.00']),
        ([['Продукт', 'Взрослый', 'Пенсионер', 'Ребенок'], ['говядина', '909.0123', '105', '1237.4']],
         ['909.01', '105.00', '1237.40'])
    ]
}


def test_hello_world():
    assert run_script('hello.py') == 'Hello, world!'


@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    expected = change_list_elements_from_list_to_str(expected)
    assert run_script('lists.py', input_data).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    expected = change_list_elements_from_list_to_str(expected)
    assert run_script('minion_game.py', [input_data]).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    expected = change_list_elements_from_list_to_str(expected)
    assert run_script('pirate_ship.py', input_data).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    expected = change_list_elements_from_list_to_str(expected)
    assert run_script('matrix_mult.py', input_data).split('\n') == expected


@pytest.mark.parametrize("input_data, expected", test_data['max_word'])
def test_max_word(input_data, expected):
    original_file_path = 'example.txt'
    backup_file_path = 'backup_example.txt'
    shutil.copy2(original_file_path, backup_file_path)
    with open(original_file_path, 'w', encoding="utf-8") as f:
        f.write(input_data)
    result = run_script('max_word.py', input_data).split('\n')
    os.remove(original_file_path)
    shutil.move(backup_file_path, original_file_path)
    assert result == expected


@pytest.mark.parametrize("input_data, expected", test_data['price_sum'])
def test_price_sum(input_data, expected):
    original_file_path = 'products.csv'
    backup_file_path = 'backup_products.csv'
    shutil.copy2(original_file_path, backup_file_path)
    with open(original_file_path, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        for line in input_data:
            writer.writerow(line)
    result = run_script('price_sum.py', input_data).split()
    os.remove(original_file_path)
    shutil.move(backup_file_path, original_file_path)
    assert result == expected
