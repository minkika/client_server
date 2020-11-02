import json
import argparse
import time

# Порт поумолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '0.0.0.0'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длина сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

# Ключ для всех клиентов
ALL_CLIENTS = 'all'
SERVER_ONLY = 'server'


def dict_to_bytes(the_dict):
    return json.dumps(the_dict, indent=2).encode(ENCODING)


def bytes_to_dict(the_binary):
    return json.loads(the_binary.decode(ENCODING))


class ErrorWrongData(Exception):
    """Исключение  - некорректные данные получены от сокета"""
    def __str__(self):
        return u'Принято некорректное сообщение от удалённого компьютера.'


class ErrorNonDict(Exception):
    """Исключение - аргумент функции не словарь"""
    def __str__(self):
        return u'Аргумент функции должен быть словарём.'


def get_message(sender, message_text, destination):
    return {
        ACTION: MESSAGE,
        SENDER: sender,
        DESTINATION: destination,
        TIME: time.time(),
        MESSAGE_TEXT: message_text
    }


def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    """
    if not isinstance(message, dict):
        raise ErrorNonDict
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, default=DEFAULT_IP_ADDRESS)
    parser.add_argument('-p', type=int, default=DEFAULT_PORT)
    parser.add_argument('-n', type=str, default='')
    return parser.parse_args()
