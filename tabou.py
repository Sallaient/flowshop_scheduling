import flowshop
import queue
from random import randint,shuffle
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

    # Test each position for a random job by interchanging it with all the other jobs
    indexes = [i for i in range(len(solution))]
    idx = indexes.pop(randint(0, len(indexes)-1))
    for i in indexes:
        neighboursList.append(solution.copy())
        neighboursList[-1][idx], neighboursList[-1][i] = neighboursList[-1][i], neighboursList[-1][idx]

    # Rotate the list of jobs 
    for i in range(1, len(solution)):
        neighboursList.append(solution[i:] + solution[:i])
    
    # print(len(neighboursList))
    return neighboursList

def tabou(flow_shop, maxTabou, printOrdo=False):

    nb_machines = flow_shop['nombre machines']
    solution_init = flow_shop['liste jobs']
    shuffle(solution_init)
    # Initialisation
    best = solution_init.copy()
    bestCandidate = solution_init.copy()

    tabouList = queue.Queue(maxsize=maxTabou)
    add_tabou(tabouList, solution_init)
    i = 0
    imax = nb_machines**5
    # print("imax = ", imax)
    while i < imax:
        i += 1
        listNeighbours = getNeighbours(bestCandidate)
        for candidate in listNeighbours:
            if candidate not in tabouList.queue:
                candidateValue = getValue(candidate, nb_machines)
                if candidateValue < getValue(bestCandidate, nb_machines):
                    # print("candidateValue = ", candidateValue)
                    bestCandidate = candidate.copy()
        if getValue(bestCandidate, nb_machines) < getValue(best, nb_machines):
            best = bestCandidate.copy()
        add_tabou(tabouList, bestCandidate)

    # Affichage
    if printOrdo:
        ordo = flowshop.creer_ordo_vide(nb_machines)
        flowshop.ordonnancer_liste_jobs(ordo,best)
        flowshop.afficher_ordo(ordo)
    else:
        print(getValue(best, nb_machines))

def tabouFromFile(fs_path, maxTabou=20, printOrdo=False):
    fs = flowshop.lire_flowshop(fs_path)
    tabou(fs, maxTabou, printOrdo=printOrdo)