#!/usr/bin/python3
# -*- coding: utf8 -*-

import time
import threading


class ClimChamber(threading.Thread):
    def __init__(self, gpio, set_temp):
        threading.Thread.__init__(self)
        self.target = set_temp
        self.gpio = gpio
        print("clim chambre - Init terminée")

        self.running = True
        self.pause = False

    def stop(self):
        self.running = False

    def run(self):

        self.running = False
        while self.running:

            pass
