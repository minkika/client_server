"""Программа-клиент"""
from socket import AF_INET, SOCK_STREAM, socket

from common.utils import create_parser, PresenceMessage, Response
from common.variables import ENCODING, MAX_PACKAGE_LENGTH
from common.decorators import log_de

import logging
import log.client_log_config

CLIENT_LOGGER = logging.getLogger('client')

class Client:
    def __init__(self, logger, user='GUEST'):
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.account_name = user
        self.logger = logger
        self.addr, self.port = create_parser()
        self.logger.info(f'Клиент создан с параметрами {self.addr} {self.port}')

    @log_de
    def create_connection(self):
        try:
            self.connection.connect((self.addr, self.port))
            self.logger.info(f'Клиент подключен с параметрами {self.addr} {self.port}')
            self.send_message(PresenceMessage(user={'account_name': self.account_name}))
        except:
            self.logger.critical(f'Не удалось подключиться к серверу')
            print('Не удалось подключиться к серверу')
            exit(1)

    # def close_connection(self):
    #     self.send_message(NonPresenceMessage(user={'account_name': self.account_name}))

    @log_de
    def send_message(self, message):
        self.logger.info(f'Отправка сообщения {message.action} от клиента {self.account_name}')
        try:
            self.connection.send(message.to_bytes())
            self.logger.info(f'Сообщение {message.action} от клиента {self.account_name} отправлено на сервер')
        except:
            self.logger.error(f'Сообщение {message.action} от клиента {self.account_name} не отправлено на сервер')

        return self.get_response()

    @log_de
    def get_response(self):
        response = Response(
            self.connection.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
        )
        self.logger.info(f'Получен ответ {response} от сервера для клиента {self.account_name}')
        return response


if __name__ == '__main__':
    client = Client(CLIENT_LOGGER)
    client.create_connection()
