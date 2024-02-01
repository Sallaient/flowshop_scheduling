import flowshop as fl
import random
from math import floor  # pour arrondir à l'entier inférieur
import time


def croisement(pop_size: int, population_origin: list, pos: int):
    """On choisit aléatoirement des élément de la population des parent que l'on croise à l'indice pos puis on les corrige et on récupère la moitié des parents et la moitié des enfants"""
    # print(population, "\n")
    population = population_origin.copy()
    new_population = [None for _ in range(pop_size)]
    for i in range(floor(pop_size/2)):
        parent1 = random.choice(population)
        population.remove(parent1)
        parent2 = random.choice(population)
        population.remove(parent2)
        enfant1 = parent1[:pos] + parent2[pos:]
        enfant2 = parent2[:pos] + parent1[pos:]
        new_population[2*i] = enfant1
        new_population[2*i+1] = enfant2
        # print(parent1,"\t",parent2,"\t",enfant1,"\t",enfant2)
    for i in range(pop_size):
        if new_population[len(new_population)-1-i] == None:
            new_population[len(new_population)-1-i] = population[i]
    for child in new_population:
        infos = [None for _ in range(len(child))]
        doublons = []
        for i in range(len(child)):
            if infos[child[i]] == None:
                infos[child[i]] = i
            else:
                doublons.append(i)
        manquants = []
        for i in range(len(infos)):
            if infos[i] == None:
                manquants.append(i)
        for doublon in doublons:
            e = random.choice(manquants)
            child[doublon] = e
            manquants.remove(e)
    population = [None for _ in range(pop_size)]

    for i in range(pop_size):
        if i % 2 == 0:
            population[i] = random.choice(population_origin)
            population_origin.remove(population[i])
        if i % 2 == 1:
            population[i] = random.choice(new_population)
            new_population.remove(population[i])
    population_origin = population
    # print("\n", population)

    return population_origin


def mutation(pop_size: int, population: list, taux_mutation: float):
    """Mutation de la population en echangeant la position de deux jobs"""
    for i in range(round(pop_size * taux_mutation)):
        mutant = random.choice(population)
        pos1, pos2 = random.randint(
            0, len(mutant)-1), random.randint(0, len(mutant)-1)
        while (pos1 == pos2):
            pos2 = random.randint(0, len(mutant)-1)
        mutant[pos1], mutant[pos2] = mutant[pos2], mutant[pos1]
    return population


def eval(population: list, flowshop, nb_machines: int, meilleur_temps: int, meilleure_solution: list):
    """evalue le meilleur temps d'une population donnée"""
    for candidat in population:
        liste_jobs = [None for _ in range(len(candidat))]
        for i in range(len(candidat)):
            for job in flowshop['liste jobs']:
                if job['numéro'] == candidat[i]:
                    liste_jobs[i] = job
        ordo = fl.creer_ordo_liste_jobs(nb_machines, liste_jobs)
        # ordo.afficher_ordo()
        # for job in liste_jobs :
        #     job.afficher_job()
        if ordo['disponibilité'][nb_machines-1] < meilleur_temps:
            meilleur_temps = ordo['disponibilité'][nb_machines-1]
            meilleure_solution = candidat
    return meilleur_temps, meilleure_solution


def recherche(pop_size: int, flowshop, taux_mutation: float, nb_iterations: int, duree=5*60):
    """méthode principale du GA pour trouver une solution optimale à un flow shop"""
    population = [None for _ in range(pop_size)]
    meilleur_temps = 10**20
    meilleure_solution = [None for _ in range(len(flowshop['liste jobs']))]
    nb_machines = flowshop['nombre machines']
    i = 0
    while i < pop_size:
        ordo_candidat = random.sample(
            range(len(flowshop['liste jobs'])), len(flowshop['liste jobs']))
        test = True
        for j in range(i):
            if population[j] == ordo_candidat:
                test = False
        if test == True:
            population[i] = ordo_candidat
            i += 1

    temps_debut = time.time()
    j = 0
    while j < nb_iterations or ((time.time()-temps_debut) < duree):
        j += 1
        pos = random.randint(0, len(flowshop['liste jobs'])-1)
        population = croisement(pop_size, population, pos)
        population = mutation(pop_size, population, taux_mutation)
        meilleur_temps, meilleure_solution = eval(
            population, flowshop, nb_machines, meilleur_temps, meilleure_solution)
    print("La meilleur solution trouvée avec l'algorithme génétique au bout de ",
          nb_iterations, " itérations est :")
    liste_jobs = [None for _ in range(len(meilleure_solution))]
    for i in range(len(meilleure_solution)):
        for job in flowshop['liste jobs']:
            if job['numéro'] == meilleure_solution[i]:
                liste_jobs[i] = job
    ordo = fl.creer_ordo_liste_jobs(nb_machines, liste_jobs)
    fl.afficher_ordo(ordo)
    print("population de ", pop_size, ".")


def genetique_from_file(path, pop_size=100, taux_mutation=0.2, nb_iterations=10000):
    flowshop = fl.lire_flowshop(path)
    recherche(pop_size, flowshop, taux_mutation, nb_iterations)
