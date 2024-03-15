import argparse
import os


def file_search(file_name: str) -> (str, bool):
    result: list[str] = []
    for root, dirs, files in os.walk('.'):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for i in range(5):
                        line = file.readline()
                        if not line:
                            break
                        result.append(line.strip())
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
            return '\n'.join(result)
    return f"Файл {file_name} не найден"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    arguments = parser.parse_args()
    print(file_search(arguments.filename))
