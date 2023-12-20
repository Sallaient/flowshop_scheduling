
__author__ = 'Chams Lahlou'
__date__ = 'Décembre 2022'
__version__ = '0.4'

import flowshop
from pprint import pprint

if __name__ == "__main__":
    fs = flowshop.lire_flowshop("jeu2-704.txt")

    machine = 2
    job = fs['liste jobs'][0]
    liste_jobs = fs['liste jobs'][1:4]
    print('\nmachine : ', machine, ', job : ', job, ', date dispo : ', flowshop.date_dispo(machine, job))
    print('\nmachine : ', machine, ', job : ', job, ', latence : ', flowshop.duree_latence(machine, job, fs['nombre machines']))
    print('\nmachine : ', machine, '\njobs : ', end='')
    pprint(liste_jobs)
    print('latence : ', flowshop.duree_jobs(machine, liste_jobs), '\n')