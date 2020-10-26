"""Программа-клиент"""
import random
import time
from socket import AF_INET, SOCK_STREAM, socket

from common.utils import ChatMessage, create_arguments_parser, PresenceMessage
from common.variables import ENCODING, MAX_PACKAGE_LENGTH
from common.decorators import log_de

import logging

CLIENT_LOGGER = logging.getLogger('client')


class Client:
    def __init__(self, logger):
        self.addr, self.port, self.client_id = create_arguments_parser()
        self.logger = logger
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.logger.info(f'Клиент {self.client_id} создан с параметрами {self.addr} {self.port}')

    @log_de
    def create_connection(self):
        try:
            self.connection.connect((self.addr, self.port))
            self.logger.info(f'Клиент подключен с параметрами {self.addr} {self.port}')
            self.send(PresenceMessage(user={'account_name': self.client_id}))
        except Exception as err:
            self.logger.critical(f'Не удалось подключиться к серверу ${err}')
            exit(1)

    @log_de
    def send(self, message):
        print('send >>>', message)
        self.logger.info(f'Отправка сообщения {message.action} от клиента {self.client_id}')

        try:
            self.connection.send(message.to_bytes())
            self.logger.info(f'Сообщение {message.action} от клиента {self.client_id} отправлено на сервер')
        except Exception as err:
            self.logger.error(f'send>')

        return self.get_response()

    @log_de
    def get_response(self):
        data = self.connection.recv(MAX_PACKAGE_LENGTH)
        response = data.decode(ENCODING)
        print('get_response >>>', response)
        self.logger.info(f'Получен ответ {response} от сервера для клиента {self.client_id}')
        return response

    @log_de
    def send_chat_message(self, text):
        print('send_chat_message', text)
        self.send(ChatMessage(text=text, user={'account_name': self.client_id}))


if __name__ == '__main__':
    client = Client(CLIENT_LOGGER)
    client.create_connection()
    client.send_chat_message(f'client {client.client_id}')
