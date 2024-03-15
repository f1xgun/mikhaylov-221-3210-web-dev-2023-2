import argparse
import os
from collections import defaultdict


def files_sort(dir_path: str) -> list[str]:
    files_by_extension: dict[str, list] = defaultdict(list)

    for file in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file)):
            extension = os.path.splitext(file)[1]
            files_by_extension[extension].append(file)

    for extension in files_by_extension:
        files_by_extension[extension].sort()

    result: list[str] = []
    for extension in sorted(files_by_extension.keys()):
        result.extend(files_by_extension[extension])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_path', type=str)
    arguments = parser.parse_args()
    print(files_sort(arguments.dir_path))
