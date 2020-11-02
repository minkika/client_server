#!/usr/bin/env python3
import threading
import socket
import os
import sys
import tkinter
from common import MAX_PACKAGE_LENGTH, parse_arguments, ENCODING, PRESENCE, SENDER, MESSAGE_TEXT, get_message, \
    ALL_CLIENTS, \
    dict_to_bytes, \
    bytes_to_dict, SERVER_ONLY

clients = [
    ALL_CLIENTS,
    "Рос",
    "Чендлер",
    "Джо",
    "Рейчел",
    "Моника",
    "Фиби"
]


def close(client):
    """
    Выходим из чата
    """
    send_message(client, '{} отключился'.format(client.client_name), ALL_CLIENTS)
    client.sock.close()
    os._exit(0)


def send_message(client, message, to):
    """
    Отправляем сообщение
    """
    formatted = get_message(client.client_name, message, to)
    # print(formatted)
    client.sock.sendall(dict_to_bytes(formatted))


def add_message(messages, message):
    """
    Добавляем сообщение в список и прокручиваем вниз
    """
    messages.insert(tkinter.END, message)
    messages.select_clear(messages.size() - 2)
    messages.select_set(tkinter.END)
    messages.yview(tkinter.END)


class Send(threading.Thread):
    def __init__(self, sock, client_name):
        super().__init__()
        self.sock = sock
        self.client_name = client_name

    def run(self):
        while True:
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            if message == 'EXIT':
                break
            else:
                send_message(self, '{}: {}'.format(self.client_name, message), ALL_CLIENTS)

        close(self)


class Receive(threading.Thread):
    def __init__(self, sock, client_name, messages):
        super().__init__()
        self.sock = sock
        self.client_name = client_name
        self.messages = messages

    def run(self):
        while True:
            message = self.sock.recv(MAX_PACKAGE_LENGTH)

            if message:
                if self.messages:
                    msg = bytes_to_dict(message)
                    print('Получено сообщение {}'.format(msg))
                    add_message(self.messages, '{}: {}'.format(msg[SENDER], msg[MESSAGE_TEXT]))
            else:
                add_message(self.messages, 'Потеряно соединение с сервером')
                close(self)


class Client:
    def __init__(self, host, port, client_name, messages):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_name = client_name
        self.messages = messages

    def start(self):
        add_message(self.messages, 'Подключаемся к {}:{}'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        send = Send(self.sock, self.client_name)
        receive = Receive(self.sock, self.client_name, self.messages)
        send.start()
        receive.start()
        send_message(self, PRESENCE, SERVER_ONLY)
        add_message(self.messages, 'Подключились!')
        return receive

    def send(self, text_input, to_input):
        message = text_input.get()
        to = to_input.get()
        text_input.delete(0, tkinter.END)

        if message == 'EXIT':
            close(self)
        else:
            add_message(self.messages, 'Вы > {}: {}'.format(to, message))
            send_message(self, message, to)


def main(host, port, client_name):
    window = tkinter.Tk()
    window.title(client_name)

    frame_messages = tkinter.Frame(master=window)
    scrollbar = tkinter.Scrollbar(master=frame_messages)
    list_messages = tkinter.Listbox(master=frame_messages, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=False)
    list_messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    client = Client(host, port, client_name, list_messages)
    receive = client.start()

    to_input = tkinter.StringVar()
    text_input = tkinter.Entry()
    client_select = tkinter.OptionMenu(window, to_input, *clients)
    to_input.set(clients[0])

    text_input.bind("<Return>", lambda x: client.send(text_input, to_input))
    text_input.focus()

    btn_send = tkinter.Button(text='Отправить', command=lambda: client.send(text_input, to_input))

    frame_messages.grid(row=0, column=0, columnspan=3, sticky="nsew")
    window.rowconfigure(0, minsize=500, weight=1)
    window.columnconfigure(0, minsize=500, weight=1)

    text_input.grid(row=1, column=0, sticky="nsew", pady=5)
    client_select.grid(row=1, column=1, sticky="nsew", pady=3)
    btn_send.grid(row=1, column=2, sticky="nsew", pady=5)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(1, minsize=100, weight=0)

    window.mainloop()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.a, args.p, args.n)
