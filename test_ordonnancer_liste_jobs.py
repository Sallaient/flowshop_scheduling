
__author__ = 'Chams Lahlou'
__date__ = 'Décembre 2022'
__version__ = '0.4'

import flowshop
from pprint import pprint

if __name__ == "__main__":
    j1 = flowshop.creer_job(1,[1,1,1,10,1])
    j2 = flowshop.creer_job(2,[1,10,1,1,1])
    l = [j1, j2]
    o = flowshop.creer_ordo_vide(5)
    flowshop.ordonnancer_liste_jobs(o, l)    

    pprint(o)
    flowshop.afficher_ordo(o)
    flowshop.afficher_job(j1)
    flowshop.afficher_job(j2)
