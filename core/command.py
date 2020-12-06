#!/usr/bin/python3
# -*- coding: utf8 -*-

import threading


class Console(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

        self.command = []
        self.running = True
        print("console - Init terminée")


    def run(self):

        while self.running:

            data = input()
            command = data.split(" ")
            if data == "QUIT":
                self.command.append("QUIT")
                print("appuyer sur entrée pour quitter")
                input()
            if command[0] == "PAUSE" and command[1] == "ALL":
                self.command.append("PAUSE ALL")
            if command[0] == "RUN" and command[1] == "ALL":
                self.command.append("RUN ALL")
            if command[0] == "SET" and command[1] == "TEMP" and\
                    command[2] == "SALON" and command[3].isdigit():
                self.command.append("SET TEMP SALON " + command[3])
                print("request set temp salon "+ command[3])


            print("vérif - Console - run")

    def stop(self):
        self.running = False
