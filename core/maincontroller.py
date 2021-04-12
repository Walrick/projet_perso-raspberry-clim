#!/usr/bin/python3
# -*- coding: utf8 -*-

import multiprocessing
import time

import core.composant.clim_controller as clim_controller
import core.gpio as gpio
import core.receiver as receiver
import core.command as command


class MainController:
    def __init__(self):

        # Init POO
        self.gpio = gpio.Gpio()

        # Init multiprocessing - new process
        print("MainController - lance l'init du processus de la clim_controller")
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.clim_controller = clim_controller.ClimControl(
            "clim_controller",
            self.child_conn,
            self.gpio
        )
        print("MainController - init du processus de la clim_controller complet")

        # Init comm inter-processing - new thread
        print("MainController - lance l'init du thread de la main receiver")
        self.receiver_main = receiver.Receiver("main receiver", self.parent_conn)
        print("MainController - init du processus de la main receiver complet")

        # Init console - new thread
        print("MainController - lance l'init du thread de la console")
        self.console = command.Console("console")
        print("MainController - init du processus de la console complet")

        # Start thread and processing
        self.receiver_main.start()
        self.clim_controller.start()
        self.console.start()

        # Init attribute
        self.running = True

        # d'après la fonction, 4 coeur sur le raspberry
        proc = multiprocessing.cpu_count()
        print("Processeurs : " + str(proc))
        print("init terminée")

    def main_loop(self):

        while self.running:

            # Loop income process
            data = self.receiver_main.data
            self.receiver_main.data = []

            for send in data:
                print(send)

            console = self.console.command
            self.console.command = []

            # Loop income command
            for send in console:
                command = send.split(" ")

                # for quit all thread and process
                if send == "QUIT":
                    self.parent_conn.send("QUIT")
                    loop = True
                    while loop:
                        self.receiver_main.stop()
                        self.console.stop()
                        self.running = False
                        self.parent_conn.send("QUIT")
                        print("main receiver is alive : " + str(self.receiver_main.is_alive()))
                        print("console is alive : " + str(self.console.is_alive()))
                        if not self.receiver_main.is_alive() and not self.console.is_alive():
                            loop = False
                        time.sleep(1)

                if send == "PAUSE ALL":
                    self.parent_conn.send("PAUSE ALL")

                if send == "RUN ALL":
                    self.parent_conn.send("RUN ALL")

                if command[0] == "SET":
                    self.parent_conn.send(send)

            time.sleep(10)
            print("vérif - MainController - run")



