#!/usr/bin/python3
# -*- coding: utf8 -*-

import threading
import time


class ClimSalon(threading.Thread):
    def __init__(self, gpio, set_temp):
        threading.Thread.__init__(self)
        self.temp_target = set_temp
        self.gpio = gpio

        self.component = Component(self.gpio)

        self.wait = 10
        self.running = True
        self.pause = False

        print("clim salon - Init terminée")

    def stop(self):
        self.running = False
        self.component.compresseur("OFF")
        self.component.fan_principal("ARRET")
        self.component.fan_secondaire("ARRET")

    def get_temp_target(self, temp_target):
        self.temp_target = temp_target

    def return_log(self):

        print(time.asctime())
        print("température salon calculé : " + str(self.temp_salon))
        print(
            "Salon : "
            + str(self.component.temp_salon)
            + ", entrée_air : "
            + str(self.component.temp_entree_air)
        )
        print(
            "Température fluide : "
            + str(self.component.temp_fluide_interne)
            + ", Véranda : "
            + str(self.component.temp_veranda)
        )
        print("température alim : " + str(self.component.temp_alim))
        print("Etat component :")
        print("Ventilateur principal : " + self.component.fan_prin)
        print("Ventilateur secondaire : " + self.component.fan_sec)
        print("Compresseur : " + self.component.compres)
        print("Inversseur : " + self.component.inver)
        print("-----------------------------------------------")

    def run(self):
        while self.running:

            self.component.temp()

            if self.pause:

                self.component.compresseur("OFF")
                self.component.fan_principal("ARRET")
                self.component.fan_secondaire("ARRET")

            else:

                self.temp_salon = (
                    self.component.temp_entree_air + self.component.temp_salon
                ) / 2
                if self.temp_target > self.temp_salon:
                    # il faut plus froid que la cible
                    self.delta = self.temp_target - self.temp_salon
                    if self.delta < 0.5:
                        self.component.fan_principal("PETITE")
                        self.component.compresseur("OFF")
                        self.component.inverseur("CHAUD")
                        self.component.fan_secondaire("PETITE")
                    elif self.delta < 2:
                        self.component.fan_principal("MOYENNE")
                        self.component.compresseur("ON")
                        self.component.inverseur("CHAUD")
                        self.component.fan_secondaire("GRANDE")
                    else:
                        self.component.fan_principal("GRANDE")
                        self.component.compresseur("ON")
                        self.component.inverseur("CHAUD")
                        self.component.fan_secondaire("GRANDE")
                if self.temp_target < self.temp_salon:
                    # il fait plus chaud que la cible
                    self.delta = self.temp_salon - self.temp_target
                    if self.delta < 0.5:
                        self.component.fan_principal("PETITE")
                        self.component.compresseur("OFF")
                        self.component.inverseur("FROID")
                        self.component.fan_secondaire("PETITE")
                    elif self.delta < 2:
                        self.component.fan_principal("MOYENNE")
                        self.component.compresseur("ON")
                        self.component.inverseur("FROID")
                        self.component.fan_secondaire("GRANDE")
                    else:
                        self.component.fan_principal("GRANDE")
                        self.component.compresseur("ON")
                        self.component.inverseur("FROID")
                        self.component.fan_secondaire("GRANDE")

            print(time.asctime())
            print("température salon calculé : " + str(self.temp_salon))
            print(
                "Salon : "
                + str(self.component.temp_salon)
                + ", entrée_air : "
                + str(self.component.temp_entree_air)
            )
            print(
                "Température fluide : "
                + str(self.component.temp_fluide_interne)
                + ", Véranda : "
                + str(self.component.temp_veranda)
            )
            print("température alim : " + str(self.component.temp_alim))
            print("Etat component :")
            print("Ventilateur principal : " + self.component.fan_prin)
            print("Ventilateur secondaire : " + self.component.fan_sec)
            print("Compresseur : " + self.component.compres)
            print("Inversseur : " + self.component.inver)
            print("-----------------------------------------------")
            time.sleep(self.wait)


class Component:
    def __init__(self, gpio):

        self.gpio = gpio
        self.timer_off = time.time()
        self.fan_prin = "ARRET"
        self.fan_sec = "ARRET"
        self.compres = "OFF"
        self.inver = "FROID"

    def temp(self):
        for capteur in self.gpio.thermometer:
            if capteur.location == "fluide_interne":
                self.temp_fluide_interne = capteur.get_value()
            if capteur.location == "Salon":
                self.temp_salon = capteur.get_value()
            if capteur.location == "entrée_d'air":
                self.temp_entree_air = capteur.get_value()
            if capteur.location == "Veranda":
                self.temp_veranda = capteur.get_value()
            if capteur.location == "Alim":
                self.temp_alim = capteur.get_value()

    def fan_principal(self, vitesse):
        if vitesse == "PETITE":
            self.gpio.write(5, 1)
            self.gpio.write(6, 1)
            self.gpio.write(3, 0)
            self.fan_prin = "PETITE"
        if vitesse == "MOYENNE":
            self.gpio.write(6, 1)
            self.gpio.write(3, 1)
            self.gpio.write(5, 0)
            self.fan_prin = "MOYENNE"
        if vitesse == "GRANDE":
            self.gpio.write(3, 1)
            self.gpio.write(5, 1)
            self.gpio.write(6, 0)
            self.fan_prin = "GRANDE"
        if vitesse == "ARRET":
            self.gpio.write(3, 1)
            self.gpio.write(5, 1)
            self.gpio.write(6, 1)
            self.fan_prin = "ARRET"

    def fan_secondaire(self, vitesse):
        if vitesse == "PETITE":
            self.gpio.write(8, 1)
            self.gpio.write(7, 0)
            self.fan_sec = "PETITE"
        if vitesse == "GRANDE":
            self.gpio.write(7, 0)
            self.gpio.write(8, 1)
            self.fan_sec = "GRANDE"
        if vitesse == "ARRET":
            self.gpio.write(7, 1)
            self.gpio.write(8, 1)
            self.fan_sec = "ARRET"

    def compresseur(self, types):
        if types == "ON":
            self.timer_on = time.time()
            result = self.timer_on - self.timer_off
            if result > 100:
                self.gpio.write(2, 0)
                self.compres = "ON"
        if types == "OFF":
            self.timer_off = time.time()
            self.gpio.write(2, 1)
            self.compres = "OFF"

    def inverseur(self, types):
        if types == "FROID":
            self.gpio.write(9, 1)
            self.inver = "FROID"

        if types == "CHAUD":
            self.gpio.write(9, 0)
            self.inver = "CHAUD"
