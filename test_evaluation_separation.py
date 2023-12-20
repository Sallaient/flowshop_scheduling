
__author__ = 'Chams Lahlou'
__date__ = 'Décembre 2022'
__version__ = '0.4'

import flowshop
from time import time

if __name__ == "__main__":
    fs = flowshop.lire_flowshop("jeu2-704.txt")
    fs = flowshop.lire_flowshop("jeu3-973.txt")
    # fs = flowshop.lire_flowshop("jeu4-844.txt")
    print()
    start = time()
    val_solution, liste_solution, _ = flowshop.evaluation_separation(fs)
    print(f'Valeur de la solution : {val_solution}')
    print(f'Ordre des numéros de jobs : {[job["numéro"] for job in liste_solution]}')
    end = time()
    print(f'Temps de calcul : {(end - start):.2f} s')