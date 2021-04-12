# Projet perso

## Mise en oeuvre d'un raspberry py pour piloter une clim

Ce projet m'a permis de piloter une clim portative grace a un raspberry py et quelques sondes de temperatures.
J'ai également pu aborder la mise en place du threading et multiprocessoring (même si pour ce projet ce n'était pas nécessaire)

## Attention
Ce projet n'est pas maintenu et il manque un fichier constant.py dans le dossier core.

Le fichier doit contenir deux dictionnaires 
  - relais_1 : 
La sortie d'un relais avec optocoupleur DOIT être à 0 pour l'activer
 et à 1 pour le désactiver, numéros de pin = cle du dictionnaire
  - position_temp :
    Position des capteurs de temperature avec leur ID (compteur de temperature de type xx-xxxxxxxxxxxx)


