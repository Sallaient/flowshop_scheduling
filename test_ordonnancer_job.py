
__author__ = 'Chams Lahlou'
__date__ = 'Décembre 2022'
__version__ = '0.4'

import flowshop
from pprint import pprint

if __name__ == "__main__":
    j1 = flowshop.creer_job(1,[1,1,1,10,1])
    o = flowshop.creer_ordo_vide(5)
    flowshop.ordonnancer_job(o, j1)    

    pprint(o)
    flowshop.afficher_ordo(o)
    flowshop.afficher_job(j1)
