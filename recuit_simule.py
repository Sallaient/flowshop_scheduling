from random import random, randint
import numpy as np
import flowshop
import time

def sol_voisine(solution):
    indexes = [i for i in range(len(solution))]
    solution_voisine = solution.copy()

    idx1 = indexes.pop(randint(0, len(indexes)-1))
    idx2 = indexes.pop(randint(0, len(indexes)-1))

    solution_voisine[idx1], solution_voisine[idx2] = solution_voisine[idx2], solution_voisine[idx1]

    return solution_voisine


def energie(solution, nb_machines):
    # solution est une liste de jobs
    ordo = flowshop.creer_ordo_vide(nb_machines)
    flowshop.ordonnancer_liste_jobs(ordo, solution)

    return ordo['disponibilité'][nb_machines-1]


def recuit_simule(fs):
    # Initialisation
    nb_machines = fs['nombre machines']
    nb_jobs = len(fs['liste jobs'])
    solution = flowshop.liste_NEH(fs)
    print("Valeur initiale :", energie(solution, nb_machines))
    
    energie_ordo = energie(solution, nb_machines)

    max_iter = 1e6
    temp = 1e14

    meilleur_sol = solution.copy()
    meilleur_energie = energie_ordo

    iter = 0
    start = time.time()
    while iter < max_iter:
        solution_voisine = sol_voisine(solution)
        energie_voisin = energie(solution_voisine, nb_machines)

        if energie_voisin < energie_ordo or random() < np.exp(-(energie_voisin-energie_ordo)/temp):
            solution = solution_voisine
            energie_ordo = energie_voisin
        
        if energie_ordo < meilleur_energie:
            meilleur_sol = solution.copy()
            meilleur_energie = energie_ordo

        temp = temp * 0.9999
        if temp < 1e-10:
            break
        
        # Fin si 
        end = time.time()
        if end - start > 60 * 5:
            break
        iter += 1

    if iter == max_iter:
        print("Max iteration reached")
    if temp < 1e-10:
        print("Temp too small")
    if end - start > 60 * 5:
        print("Time limit reached")
    
        
    return meilleur_sol, meilleur_energie


def iter_recuit_simule(fs_path, nb_iter_recuit=10):
    fs = flowshop.lire_flowshop(fs_path)
    optimum = int(fs_path.split('-')[1].split('.')[0]) # Ou meilleure valeure connue

    valeurs_sol = []
    solutions = []
    erreurs = []

    for i in range(nb_iter_recuit):
        
        sol, energie = recuit_simule(fs)
        valeurs_sol.append(energie)
        erreurs.append((energie - optimum)/optimum)
        solutions.append(sol)
        
        print(f'energie: {energie}, erreur : {erreurs[-1]*100:.2f}%')
    
    print(f'meilleure solution : {[job["numéro"] for job in solutions[np.argmin(valeurs_sol)]]} valeur : {min(valeurs_sol)}, erreur : {min(erreurs)*100:.2f}%')
    print(f'erreur moyenne : {np.mean(erreurs)*100:.2f}%')
    return valeurs_sol, erreurs


if __name__ == "__main__":
    # fs_path = "tai01-1278.txt"
    # fs_path = "tai11-1582.txt"
    # fs_path = "tai21-2297.txt"
    # fs_path = "tai31-2724.txt"
    # fs_path = "tai41-2991.txt"
    fs_path = "tai51-3874.txt"

    fs = flowshop.lire_flowshop(fs_path)

    start = time.time()
    meilleur_sol, meilleur_energie = recuit_simule(fs)
    end = time.time()

    print([job['numéro'] for job in meilleur_sol], meilleur_energie)
    print(f'{end - start:.2f} s')