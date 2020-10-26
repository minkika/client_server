"""Программа-сервер"""
import json
import logging
import select
from socket import AF_INET, SOCK_STREAM, socket
from common.utils import create_arguments_parser
from common.variables import ENCODING, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH
from common.decorators import log_de

RESPONSE_ERROR = 400
RESPONSE_OK = 200

SERVER_LOGGER = logging.getLogger('server')


class Server:
    def __init__(self, logger):
        self.logger = logger
        self.transport = socket(AF_INET, SOCK_STREAM)
        # self.transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.addr, self.port, self.client_id = create_arguments_parser()
        self.logger.info(f'Сервер создан с параметрами {self.addr} {self.port}')
        print(f'Сервер создан с параметрами {self.addr} {self.port}')
        self.clients = []
        self.messages = []

    @log_de
    def create_connection(self):
        try:
            self.transport.bind((self.addr, self.port))
        except Exception as e:
            self.logger.critical(f'Сервер не подключен {e}')
            exit(1)
        finally:
            self.transport.listen(MAX_CONNECTIONS)

            while True:
                try:
                    client, client_address = self.transport.accept()
                except OSError:
                    pass
                else:
                    self.logger.info(f'Подключен клиент {client.fileno()} {client_address}')
                    self.clients.append(client)
                finally:
                    self.process_queue()

    def read_requests(self, pending):
        responses = {}

        for client in pending:
            try:
                data = client.recv(MAX_PACKAGE_LENGTH)
                if data:
                    message = json.loads(data.decode(ENCODING))
                    print(f'message >>> ${message}')
                responses[client] = data
            except Exception as err:
                print(f'read_requests >>> ${err}')
                print('Клиент {} {} отключился'.format(client.fileno(), client.getpeername()))
                self.clients.remove(client)

        return responses

    def write_responses(self, requests, pending):
        for client in pending:
            if client in requests:
                try:
                    response = requests[client]
                    print('Отвечаем {} сообщением {}'.format(client.fileno(), response))
                    client.send(response)
                except Exception as err:
                    print(f'write_responses >>> ${err}')
                    print('Клиент {} {} отключился'.format(client.fileno(), client.getpeername()))
                    client.close()
                    self.clients.remove(client)

    @log_de
    def process_queue(self):
        wait = 1
        read_list = []
        write_list = []
        err_list = []
        try:
            if self.clients:
                read_list, write_list, err_list = select.select(self.clients, self.clients, [], wait)
        except OSError:
            pass

        requests = self.read_requests(read_list)
        if requests:
            self.write_responses(requests, write_list)


def main():
    server = Server(SERVER_LOGGER)
    server.create_connection()


if __name__ == '__main__':
    main()
