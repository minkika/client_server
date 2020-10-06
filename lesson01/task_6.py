TEST_STRINGS = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w+', encoding='utf-8') as to_file:
    for string in TEST_STRINGS:
        to_file.write(f'{string}\n')


with open('test_file.txt', 'r', encoding='utf-8') as from_file:
    for line in from_file:
        print(line)