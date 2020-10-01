"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но отерыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""

TEST_STRINGS = ['сетевое программирование', 'сокет', 'декоратор']


with open('test_file.txt', 'w+') as to_file:
    for string in TEST_STRINGS:
        to_file.write(f'{string}\n')
    print(type(to_file))


with open('test_file.txt', 'r', encoding='utf-8') as from_file:
    for line in from_file:
        print(line)
