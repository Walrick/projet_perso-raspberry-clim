#!/usr/bin/python3.9
# -*- coding: utf8 -*-

import threading


class Receiver(threading.Thread):
    def __init__(self, name, conn_pipe):
        threading.Thread.__init__(self)
        self.name = name
        self.conn_pipe = conn_pipe

        self.data = []
        self.running = True
        print(self.name + " - Init terminée")

    def run(self):
        while self.running:

            data = self.conn_pipe.recv()
            self.data.append(data)
            print("Réception de donnée sur le thread " + self.name)
            print(self.data, data)

    def stop(self):
        self.running = False

