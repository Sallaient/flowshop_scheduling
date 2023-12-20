
__author__ = 'Chams Lahlou'
__date__ = 'Décembre 2022'
__version__ = '0.4'

import flowshop
from pprint import pprint

if __name__ == "__main__":
    fs = flowshop.lire_flowshop("jeu2-704.txt")

    l_NEH = flowshop.liste_NEH(fs)
    ordo = flowshop.creer_ordo_vide(fs['nombre machines'])

    print("Numéros des jobs restants :", [job['numéro'] for job in l_NEH], "Evalutation : ", flowshop.eval(ordo, l_NEH))

    n = 8
    jobs_places = l_NEH[:n]
    jobs_restants = l_NEH[n:]
    flowshop.ordonnancer_liste_jobs(ordo, jobs_places)

    print("Numéros des jobs restants :", [job['numéro'] for job in jobs_restants], "Evalutation : ", flowshop.eval(ordo, jobs_restants))
