"""Программа-клиент"""
from socket import AF_INET, SOCK_STREAM, socket

from common.utils import create_parser, PresenceMessage, print_error, Response
from common.variables import ENCODING, MAX_PACKAGE_LENGTH


class Client:
    def __init__(self, user='GUEST'):
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.account_name = user
        self.addr, self.port = create_parser()

    def create_connection(self):
        self.connection.connect((self.addr, self.port))
        self.send_message(PresenceMessage(user={'account_name': self.account_name}))

    # def close_connection(self):
    #     self.send_message(NonPresenceMessage(user={'account_name': self.account_name}))

    def send_message(self, message):
        print('send', message, message.to_bytes())
        try:
            self.connection.send(message.to_bytes())
        except:
            print_error('Ошибка при отправке')

        return self.get_response()

    def get_response(self):
        response = Response(
            self.connection.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
        )

        print('response >>>', response)
        return response


if __name__ == '__main__':
    client = Client()
    client.create_connection()
