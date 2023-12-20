from random import random, randint
import numpy as np
import flowshop

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


def recuit_simule(solution_init, nb_machines, max_iter=1000, energie_max=100, temp_init = 100):
    
    # Initialisation
    solution = solution_init.copy()
    energie_ordo = energie(solution_init, nb_machines)
    temp = temp_init
    iter = 0

    meilleur_sol = solution_init.copy()
    meilleur_energie = energie_ordo

    # while iter < max_iter and energie_ordo > energie_max:
    while iter < max_iter:
        solution_voisine = sol_voisine(solution)
        energie_voisin = energie(solution_voisine, nb_machines)

        if energie_voisin < energie_ordo or random() < np.exp(-(energie_voisin-energie_ordo)/temp):
            solution = solution_voisine
            energie_ordo = energie_voisin
        
        if energie_ordo < meilleur_energie:
            meilleur_sol = solution.copy()
            meilleur_energie = energie_ordo
            # print(f'iter : {iter}, energie : {energie_ordo}')


        temp = temp_init * 0.99
        iter += 1

    return meilleur_sol, meilleur_energie


def erreur(fs_path, max_iter=1e4, temp_init = 1e6, nb_iter=20):
    fs = flowshop.lire_flowshop(fs_path)
    optimum = int(fs_path.split('-')[1].split('.')[0])

    erreurs = []
    for i in range(nb_iter):
        l_NEH = flowshop.liste_NEH(fs)
        sol, energie = recuit_simule(l_NEH, fs['nombre machines'], max_iter=max_iter, temp_init=temp_init)
        erreurs.append(abs((optimum - energie)/optimum))
        
        print(f'energie: {energie}, erreur : {erreurs[-1]*100:.2f}%')
    
    print(f'erreur moyenne : {np.mean(erreurs)*100:.2f}%')


if __name__ == "__main__":
    # solution_init = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # print(sol_voisine(solution_init))

    # fs = flowshop.lire_flowshop("jeu4-844.txt")
    # l_NEH = flowshop.liste_NEH(fs)
    
    # print(recuit_simule(l_NEH, fs['nombre machines'], max_iter=1e5, temp_init=1e6))

    # fs_path = "jeu2-704.txt"
    # fs_path = "jeu3-973.txt"
    fs_path = "jeu4-844.txt"
    erreur(fs_path, max_iter=1e5, temp_init=1e6, nb_iter=20)