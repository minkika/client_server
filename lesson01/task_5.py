"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet
"""

import subprocess

import chardet


class Host:
    def __init__(self, host, process='ping'):
        self.args = [process, host]

    def open_process(self, lines=5):
        self.process = subprocess.Popen(self.args, stdout=subprocess.PIPE)
        for num, line in enumerate(self.process.stdout):
            if num == lines:
                self.process.kill()
            stdout_encoding = chardet.detect(line)['encoding']
            output = line.decode(stdout_encoding).encode('utf-8')
            print(output.decode('utf-8'))


YA_HOST = Host('youtube.com')
YA_HOST.open_process()
