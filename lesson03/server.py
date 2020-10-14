"""Программа-сервер"""
import json
from socket import AF_INET, SOCK_STREAM, socket

from utils import create_parser, print_error
from variables import ENCODING, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH


RESPONSE_ERROR = 400
RESPONSE_OK = 200


class Server:
    def __init__(self):
        self.transport = socket(AF_INET, SOCK_STREAM)
        self.addr, self.port = create_parser()

    def create_connection(self):
        self.transport.bind((self.addr, self.port))
        self.transport.listen(MAX_CONNECTIONS)

        while True:
            client, client_address = self.transport.accept()
            response = RESPONSE_ERROR
            try:
                data = client.recv(MAX_PACKAGE_LENGTH)
                if data:
                    json_answer = data.decode(ENCODING)
                    response = self.process_client_message(json.loads(json_answer))
            except:
                print_error('Принято некорректное сообщение от клиента')
            finally:
                print(f'Отвечаем клиенту', response)
                client.send(f'{response}'.encode(ENCODING))
                client.close()

    def process_client_message(self, message):
        print('process_client_message', message)
        if message['action'] == 'presence' and message['user']['account_name'] == 'GUEST':
            return RESPONSE_OK
        return RESPONSE_ERROR


def main():
    server = Server()
    server.create_connection()


if __name__ == '__main__':
    main()
