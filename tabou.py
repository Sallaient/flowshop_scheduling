import flowshop
import queue
from random import randint
import numpy as np


def add_tabou(tabouList, sol):
    if tabouList.full():
        tabouList.get()
    tabouList.put(sol)


def getValue(solution, nb_machines):
    # solution est une liste de jobs
    ordo = flowshop.creer_ordo_vide(nb_machines)
    flowshop.ordonnancer_liste_jobs(ordo, solution)

    return ordo['disponibilité'][nb_machines-1]


def getNeighbours(solution):
    neighboursList = []
    indexes = [i for i in range(len(solution))]
    idx = indexes.pop(randint(0, len(indexes)-1))
    for i in indexes:
        neighboursList.append(solution.copy())
        neighboursList[-1][idx], neighboursList[-1][i] = neighboursList[-1][i], neighboursList[-1][idx]
    return neighboursList


def tabou(flow_shop, maxTabou=20):

    nb_machines = flow_shop['nb_machines']
    solution_init = flowshop.liste_NEH(flow_shop)
    # Initialisation
    best = solution_init.copy()
    bestCandidate = solution_init.copy()
    tabouList = queue.Queue(maxsize=maxTabou)
    add_tabou(tabouList, solution_init)
    i = 0
    while i < nb_machines**5:
        i += 1
        listNeighbours = getNeighbours(bestCandidate)
        bestCandidateValue = - np.inf
        for candidate in listNeighbours:
            if candidate not in tabouList:
                candidateValue = getValue(candidate, nb_machines)
                if candidateValue > bestCandidateValue:
                    bestCandidate = candidate.copy()
                    bestCandidateValue = candidateValue
        if bestCandidateValue == - np.inf:
            break
        if getValue(bestCandidate, nb_machines) > getValue(best, nb_machines):
            best = bestCandidate.copy()
        add_tabou(tabouList, bestCandidate)

    return best, getValue(best, nb_machines)


def tabouFromFile(fs_path, maxTabou=20):
    fs = flowshop.lire_flowshop(fs_path)
    return tabou(fs, maxTabou)