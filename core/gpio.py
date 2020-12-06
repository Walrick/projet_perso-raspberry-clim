#!/usr/bin/python3
# -*- coding: utf8 -*-

import os
import core.constant as constant


class Gpio:
    def __init__(self):

        # Raspberry Pi rev 3, pin "4" en mode Wire 1
        self.legal_pins = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                           17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

        # Init des pin's
        for pin in self.legal_pins:
            if not os.path.isfile("/sys/class/gpio/gpio%i/direction" % pin):
                path = "/sys/class/gpio/export"
                content = str(pin)
                with open(path, 'w') as file:
                    file.write(content)

        # init les pin's du module relais_1 en sortie
        for pin in constant.relais_1.keys():
            path = "/sys/class/gpio/gpio%i/direction" % pin
            content = "out"
            with open(path, 'w') as file:
                file.write(content)
            path = "/sys/class/gpio/gpio%i/value" % pin
            content = "1"
            with open(path, 'w') as file:
                file.write(content)

        # init des capteurs wire 1
        directory = os.listdir("/sys/bus/w1/devices")
        sensor_nbr = len(directory) - 1
        print("nombre de capteur sur le Wire 1 : " + str(sensor_nbr))

        self.thermometer = []
        for file in directory:
            if not file == "w1_bus_master1":
                location = ""
                path = "/sys/bus/w1/devices/" + file + "/w1_slave"
                with open(path, 'r') as files:
                    data = files.read()
                prep = data.split(" ")
                temp = int(prep[20][2:]) / 1000

                for i in constant.position_temp.keys():
                    if constant.position_temp[i] == file:
                        location = i

                if location == "":
                    location = "non defini"
                    self.thermometer.append(Thermometer(location, file, temp))
                else:
                    self.thermometer.append(Thermometer(location, file, temp))
                print(location, file, temp)

    def write(self, pin, state):

        if pin in self.legal_pins:
            if state in (1, 0):
                state = str(state)
                path = "/sys/class/gpio/gpio%i/value" % pin
                with open(path, 'w') as file:
                    file.write(state)
            else:
                raise ValueError(
                    "Etat du pin {} non valide, état : {}".format(pin, state))
        else:
            raise ValueError("Pin selectionné non valide : %i" % pin)

    def read(self, pin):

        if pin in self.legal_pins:
            path = "/sys/class/gpio/gpio%i/value" % pin
            with open(path, 'r') as file:
                s = file.read()
            s = s[0]
            state = int(s)
            if state in (1, 0):
                return state
            else:
                raise ValueError(
                    "Etat du pin {} non valide, état : {}".format(pin, state))
        else:
            raise ValueError("Pin selectionné non valide : %i" % pin)

    def mode(self, pin, mode):

        if pin in self.legal_pins:
            if mode in ("in", "out"):
                path = "/sys/class/gpio/gpio%i/direction" % pin
                with open(path, 'w') as file:
                    file.write(mode)
            else:
                raise ValueError(
                    "Mode du pin {} non valide, mode : {}".format(pin, mode))
        else:
            raise ValueError("Pin selectionné non valide : %i" % pin)


class Thermometer:
    def __init__(self, location, code, value):
        self.location = location
        self.value = value
        self.code = code

    def get_value(self):
        path = "/sys/bus/w1/devices/" + self.code + "/w1_slave"
        with open(path, 'r') as files:
            data = files.read()
        prep = data.split(" ")
        self.value = int(prep[20][2:]) / 1000
        return self.value
