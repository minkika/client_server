"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import re


def get_data(files):
    result = {
        'Изготовитель системы': [],
        'Название ОС': [],
        'Код продукта': [],
        'Тип системы': []
    }
    main_data = [[*result.keys()]]

    for i in range(len(files)):
        main_data.append([i + 1])

    re_whitelist = re.compile(r'^(Изготовитель системы|Название ОС|Код продукта|Тип системы)')

    for file in files:
        with open(file, 'r', encoding='windows-1251') as f:
            for line in f:
                pairs = line.split(':')
                for pair in pairs:
                    if re_whitelist.search(pair):
                        result[pair].append(pairs[1].strip())

    for record in result.values():
        for num, v in enumerate(record):
            main_data[num + 1].append(record[num])

    return main_data


def write_to_csv(csv_file='data_report.csv'):
    data = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])
    with open(csv_file, 'w') as final_file:
        writer = csv.writer(final_file)
        for row in data:
            writer.writerow(row)


write_to_csv()
