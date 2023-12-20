#!/usr/bin/env python

""" Classe Sommet :

A utiliser avec une file de priorité (heapq)
dans une résolution par évaluation et séparation.

Chaque sommet contient 4 éléments :
- la liste des jobs placés
- la liste des jobs non placés
- l'évaluation
- le numéro de sommet

"""

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019 - novembre 2023'
__version__ = '0.5'

class Sommet():

    def __init__(self, places, non_places, evaluation, numero):
        # liste des jobs déjà placés
        self.places = places

        # liste des jobs qui ne sont pas encore placés
        self.non_places = non_places

        # valeur de la fonction d'évaluation pour le sommet
        self.evaluation = evaluation

        # numéro du sommet
        self.numero = numero


    def __lt__(self, sommet):
        """ permet d'utiliser les fonctions de tri de python 
        en comparant deux sommets selon l'attribut 'valeur' 
        """
        return self.evaluation < sommet.evaluation
