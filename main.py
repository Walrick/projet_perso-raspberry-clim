#!/usr/bin/python3
# -*- coding: utf8 -*-

import core.controller as controller


class Main:
    def __init__(self):
        self.controller = controller

    def launch(self):
        self.controller.main_loop()


if __name__ == '__main__':
    main = Main()
    main.launch()
