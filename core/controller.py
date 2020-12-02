#!/usr/bin/python3
# -*- coding: utf8 -*-

import core.gpio as gpio


class Controller:
    def __init__(self):

        self.gpio = gpio.Gpio()

        self.running = True

    def main_loop(self):

        while self.running:
            pass