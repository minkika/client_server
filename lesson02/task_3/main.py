"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml

data = {
    'key1': ['list', 'list', 'list', 'list'],
    'key2': 4,
    'key3': {
        'sub_key1': '1€',
        'sub_key2': '1€',
        'sub_key3': '1€',
        'sub_key4': '1€'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as to_file:
    yaml.dump(data, to_file, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as from_file:
    new_data = yaml.load(from_file, Loader=yaml.SafeLoader)

print(new_data)
