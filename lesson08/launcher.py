#!/usr/bin/env python3
import subprocess
from tkinter import Entry, Button, Tk, Label, StringVar
from common import DEFAULT_IP_ADDRESS, DEFAULT_PORT

processes = []
clients = [
    "Рос",
    "Чендлер",
    "Джо",
    "Рейчел",
    "Моника",
    "Фиби"
]


class Launcher:
    def __init__(self, master):
        self.master = master
        self.master.title('Launcher')
        self.transport = None

        self.host = StringVar()
        self.port = StringVar()
        self.clients = StringVar()
        self.msg_text = StringVar()
        self.msg_client = StringVar()

        self.host_label = Label(self.master, text='host:')
        self.port_label = Label(self.master, text='port:')
        self.clients_label = Label(self.master, text='clients:')
        self.port_entry = Entry(textvariable=self.port)
        self.clients_entry = Entry(textvariable=self.clients)
        self.host_entry = Entry(textvariable=self.host)
        self.start_button = Button(text="Запуск сервера", command=lambda: self.start())
        self.start_clients_button = Button(text="Запуск клиентов", command=lambda: self.start_clients())
        self.stop_button = Button(text="Закрыть все", command=lambda: self.stop())

        self.host_label.grid(row=0, column=0)
        self.port_label.grid(row=1, column=0)
        self.host_entry.grid(row=0, column=1)
        self.port_entry.grid(row=1, column=1)
        self.clients_label.grid(row=2, column=0)
        self.clients_entry.grid(row=2, column=1)
        self.start_button.grid(row=0, column=2, padx=5, pady=5)
        self.start_clients_button.grid(row=1, column=2, padx=5, pady=5)
        self.stop_button.grid(row=2, column=2, rowspan=2, padx=5, pady=5)

        self.host_entry.insert(0, DEFAULT_IP_ADDRESS)
        self.port_entry.insert(0, DEFAULT_PORT)
        self.clients_entry.insert(0, 2)

        master.mainloop()

    def start_clients(self):
        for i in range(int(self.clients.get())):
            processes.append(
                subprocess.Popen(
                    f'python3 client.py -a {self.host.get()} -p {self.port.get()} -n {clients[i]}',
                    shell=True,
                    encoding='utf8'
                )
            )

    def start(self):
        """ Стартуем подпроцессы """
        processes.append(
            subprocess.Popen(
                f'python3 server.py -a {self.host.get()} -p {self.port.get()}',
                shell=True,
                encoding='utf8'
            )
        )

    def stop(self):
        """ Останавливаем подпроцессы """
        while processes:
            victim = processes.pop()
            print('kill', victim.pid)
            victim.kill()
            # os.killpg(os.getpgid(victim.pid), signal.SIGHUP)
            # os.killpg(os.getpgid(victim.pid), signal.SIGTERM)


if __name__ == '__main__':
    Launcher(Tk())
