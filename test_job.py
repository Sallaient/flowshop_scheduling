#!/usr/bin/env python

__author__ = 'Chams Lahlou'
__date__ = 'Décembre 2022'
__version__ = '0.4'

import flowshop

# Pour tester
if __name__ == "__main__":
    j1 = flowshop.creer_job(2, [10,13,25,8,3])
    flowshop.afficher_job(j1)
