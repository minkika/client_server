#!/usr/bin/env python3
import threading
import socket
import os
from common import MAX_PACKAGE_LENGTH, parse_arguments, bytes_to_dict, SENDER, ALL_CLIENTS, \
    DESTINATION, SERVER_ONLY

sender_connection = {}


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(1)
            print('Сервер подключен: {}'.format(sock.getsockname()))
        except Exception as err:
            print('Ошибка {}'.format(err))
            os._exit(1)

        while True:
            # получаем запрос на соединение
            sc, name = sock.accept()
            server_socket = ServerSocket(sc, name, self)
            server_socket.start()
            # и сохраняем в подключениях
            self.connections.append(server_socket)

    def send(self, message, source):
        for connection in self.connections:
            if connection.sockname != source:
                # отправляем сообщение всем клиентам, кроме отправившего
                msg = bytes_to_dict(message)
                print('Разбираем сообщение для {}: {}'.format(connection.sockname, msg))

                if msg[DESTINATION] == SERVER_ONLY:
                    print('Регистрируем клиента {}'.format(msg[SENDER]))
                    sender_connection[msg[SENDER]] = connection
                elif msg[DESTINATION] == ALL_CLIENTS:
                    print('Сообщение для всех')
                    connection.send(message)
                elif msg[DESTINATION] in sender_connection.keys():
                    print('Приватное сообщение для {}'.format(msg[DESTINATION]))
                    sender_connection[msg[DESTINATION]].send(message)
                else:
                    print('Фигня какая-то')


class ServerSocket(threading.Thread):
    def __init__(self, transport, sockname, server):
        super().__init__()
        self.transport = transport
        self.sockname = sockname
        self.server = server

    def run(self):
        while True:
            message = self.transport.recv(MAX_PACKAGE_LENGTH)
            if message:
                # при сообщении
                self.server.send(message, self.sockname)
            else:
                # при отключении
                self.transport.close()
                server.connections.remove(self)
                return

    def send(self, message):
        self.transport.sendall(message)


def close(serv):
    while True:
        command = input('')
        if command == 'q':
            for connection in serv.connections:
                connection.transport.close()
            os._exit(0)


if __name__ == '__main__':
    args = parse_arguments()
    server = Server(args.a, args.p)
    server.start()
    threading.Thread(target=close, args=(server,)).start()

# lsof -i :7777