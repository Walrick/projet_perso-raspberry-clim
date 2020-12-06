#!/usr/bin/python3
# -*- coding: utf8 -*-

import core.maincontroller as main_controller


class Main:
    def __init__(self):
        self.controller = main_controller.MainController()

    def launch(self):
        self.controller.main_loop()


if __name__ == '__main__':
    main = Main()
    main.launch()
