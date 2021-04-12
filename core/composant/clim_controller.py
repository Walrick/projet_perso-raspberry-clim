#!/usr/bin/python3
# -*- coding: utf8 -*-

import multiprocessing
import time

import core.receiver as receiver
import core.composant.clim_salon as compo_salon
import core.composant.clim_chamber as clim_chamber


class ClimControl(multiprocessing.Process):
    def __init__(self, name, conn_pipe, gpio):
        multiprocessing.Process.__init__(self)
        self.name = name
        self.conn_pipe = conn_pipe
        self.gpio = gpio

        self.TEMP_SETPOINT_SALON = 18
        self.TEMP_SETPOINT_CHAMBER = 18

        self.running = True
        print(self.name + "- Init terminée")

    def run(self):

        """Init des threads, a placer dans la boucle
        sinon les threads ne sont pas reconnu dans l'init"""
        # Init comm inter-processing - new thread
        print(self.name + "- lance l'init du thread de la clim receiver")
        self.receiver_clim = receiver.Receiver("clim receiver", self.conn_pipe)
        print(self.name + "- init du thread de la clim receiver complet")

        # Init clim_salon - new thread
        print(self.name + "- lance l'init du thread de la clim_salon")
        self.clim_salon = compo_salon.ClimSalon(self.gpio, self.TEMP_SETPOINT_SALON)
        print(self.name + "- init du thread de la clim_salon complet")

        # Init clim_chamber - new thread
        print(self.name + "- lance l'init du thread de la clim_chamber")
        self.clim_chamber = clim_chamber.ClimChamber(
            self.gpio, self.TEMP_SETPOINT_CHAMBER
        )
        print(self.name + "- init du thread de la clim_chamber complet")

        self.receiver_clim.start()
        self.clim_salon.start()
        self.clim_chamber.start()

        while self.running:

            # Read data
            data = self.receiver_clim.data
            self.receiver_clim.data = []

            for send in data:
                command = send.split(" ")
                print(send, command)
                if send == "QUIT":
                    print(self.name + "- arrêt des threads")
                    loop = True
                    while loop:
                        self.receiver_clim.stop()
                        self.clim_salon.stop()
                        self.clim_chamber.stop()
                        self.running = False
                        self.conn_pipe.send("QUIT Process")
                        print(
                            "clim receiver is alive : "
                            + str(self.receiver_clim.is_alive())
                        )
                        print(
                            "clim_salon is alive : " + str(self.clim_salon.is_alive())
                        )
                        print(
                            "clim_chamber is alive : "
                            + str(self.clim_chamber.is_alive())
                        )
                        if (
                            not self.receiver_clim.is_alive()
                            and not self.clim_salon.is_alive()
                            and not self.clim_chamber.is_alive()
                        ):
                            loop = False
                        time.sleep(1)

                if send == "PAUSE ALL":
                    self.clim_salon.pause = True
                    self.clim_chamber.pause = True
                    print("pause all")

                if send == "RUN ALL":
                    self.clim_salon.pause = False
                    self.clim_chamber.pause = False
                    print("reprise")

                if (
                    command[0] == "SET"
                    and command[1] == "TEMP"
                    and command[2] == "SALON"
                ):
                    temp = int(command[3])
                    self.clim_salon.get_temp_target(temp)
                    print("set temp salon " + command[3] + " terminée")

            time.sleep(10)
            print("vérif - " + self.name + " - run")
