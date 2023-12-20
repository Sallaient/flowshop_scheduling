#!/usr/bin/env python

__author__ = 'Chams Lahlou'
__date__ = 'Octobre 2019 - novembre 2023'
__version__ = '0.5'

"""Résolution du flowshop de permutation : 

 - par l'algorithme NEH
 - par évaluation et séparation
 """

# La résolution par évaluation et séparation utilise une file de priorité pour 
# stocker et trier les sommets. Python propose le module 'heapq' :
import heapq

# On utilise deux fonctions du module 'heapq' :
#
# La fonction 'heappop' permet de récupérér le sommet de plus petite valeur. Par
# exemple : sommet = heapq.heappop(file_priorite)
#
# La fonction 'heappush' permet d'ajouter un nouveau sommet. Par exemple : 
# heapq.heappush(file_priorite, sommet)

# La structure de données des sommets est définie dans un module :
import sommet

# valeur (arbitraire) maximale d'un entier
MAXINT = 100000

'''
Fonctions pour un job
'''

def creer_job(numero_job, duree_op):
    ''' - numero_job = numéro du job
        - duree_op = liste des durées des opérations du job
        - début = liste des date de début des opérations du job
    '''

    return {'numéro':numero_job, 
            'durée':duree_op,
            'début':[None for i in duree_op]}

def afficher_job(job):
    print("Job n°", job['numéro'], 
            "de durée totale", sum(job['durée']), ":")
    
    nb_op = len(job['durée'])
    for numero in range(nb_op):
        print("  opération n°", numero, ": durée =", job['durée'][numero],
                "démarre à", job['début'][numero])

'''
Fonctions pour un ordonnancement
'''

def creer_ordo_vide(nb_mach):
    ''' renvoie un ordonnancement avec 'nb_mach' machines vides.

        - séquence = la liste des jobs ordonnancés.
        - disponibilité = la liste des dates de fin de l'ordonnancement pour 
          chaque machine.
    '''

    date_dispo = [0 for i in range(nb_mach)]
    return {'séquence':[], 'disponibilité':date_dispo}


def afficher_ordo(ordo):
    print("Ordre des jobs :", end='')
    for job in ordo['séquence']:
        print(" ", job['numéro']," ", end='')

    print()

    nb_machines = len(ordo['disponibilité'])
    for job in ordo['séquence']:
        print("Job", job['numéro'], ":", end='')

        
        for machine in range(nb_machines):
            print(" op", machine, 
                  "à t =", job['début'][machine],
                  "|", end='')

        print()
        
    print("Cmax =", ordo['disponibilité'][nb_machines-1])

################################################################################
# exo 1 :
################################################################################
def ordonnancer_job(ordo, job) -> None:
    ''' Ajoute le job 'job' à l'ordonnancemement 'ordo' à la suite des jobs
        déjà placés.
    '''
    # Modification de la liste des jobs
    ordo['séquence'].append(job)

    # Modification de la liste des dates de disponibilité
    nb_mach = len(ordo['disponibilité'])
    for machine in range(nb_mach):

        # Si c'est le premier job à ordonnacer, toutes les disponibilités sont a None
        if ordo['disponibilité'][machine] == None:

            # On sépare les cas car la première machine peut enchaîner les jobs
            if machine == 0:
                job['début'][machine] = 0
                ordo['disponibilité'][machine] = job['durée'][machine]
            else:
                job['début'][machine] = ordo['disponibilité'][machine-1]
                ordo['disponibilité'][machine] = job['durée'][machine]

        # Dès le 2ème job, on est dans ce cas
        elif ordo['disponibilité'][machine] >= 0:

            # On sépare les cas car la première machine peut enchaîner les jobs
            if machine == 0:
                job['début'][machine] = ordo['disponibilité'][machine]
            else: 
                job['début'][machine] = max(ordo['disponibilité'][machine], ordo['disponibilité'][machine-1])
            ordo['disponibilité'][machine] = job['début'][machine] + job['durée'][machine]



################################################################################
# exo 2 :
################################################################################
def ordonnancer_liste_jobs(ordo, liste_jobs):
    ''' Ajoute les jobs de la liste 'liste_jobs' à l'ordonnancemement 'ordo'
        à la suite des jobs déjà placés.
    '''

    for job in liste_jobs:
        ordonnancer_job(ordo, job)


'''
Fonctions pour un flowshop
'''

def creer_flowshop(liste_jobs=[], nb_machines=0):
    ''' - liste jobs = liste des jobs du problème
        - nombre machines : nombre de machines du problème
    '''

    return {'liste jobs':liste_jobs,
            'nombre machines':nb_machines
            }

def lire_flowshop(nom_fichier):
    """ crée un problème de flowshop à partir d'un fichier """

    # ouverture du fichier en mode lecture
    flowshop = creer_flowshop()

    fdonnees = open(nom_fichier,"r")
    # lecture de la première ligne
    ligne = fdonnees.readline() 
    l = ligne.split() # on récupère les valeurs dans une liste
    nb_jobs = int(l[0])

    nb_machines = int(l[1])
    flowshop['nombre machines'] = nb_machines
    
    flowshop['liste jobs'] = []
    # création des jobs
    for num in range(nb_jobs):
        ligne = fdonnees.readline() 
        l = ligne.split()
        # on transforme la suite de chaînes de caractères représentant
        # les durées des opérations en une liste d'entiers
        l_op = [int(d_op) for d_op in l]
        # puis on crée le job
        job = creer_job(num, l_op)
        flowshop['liste jobs'].append(job)
    # fermeture du fichier
    fdonnees.close()
    return flowshop
        
  
################################################################################
# exo 3 :
################################################################################
def liste_NEH(flow_shop):
    ''' Renvoie la liste obtenue par l'algorithme NEH pour le problème défini
        par 'flow_shop'.
    '''
    nb_machines = flow_shop['nombre machines']
    l_NEH = sorted(flow_shop['liste jobs'], key=lambda job: sum(job['durée']))
    seq_NEH = [l_NEH.pop(0)]
    len_places = 1
    for job in l_NEH:

        for i in range(len_places):
            ordo1 = creer_ordo_vide(nb_machines)
            seq_NEH1 = seq_NEH[:i] + [job] + seq_NEH[i:]
            ordonnancer_liste_jobs(ordo1, seq_NEH1)

            ordo2 = creer_ordo_vide(nb_machines)
            seq_NEH2 = seq_NEH[:i+1] + [job] + seq_NEH[i+1:]
            ordonnancer_liste_jobs(ordo2, seq_NEH2)

            if ordo1['disponibilité'][nb_machines-1] < ordo2['disponibilité'][nb_machines-1]:
                seq_NEH = seq_NEH1.copy()
            else:
                seq_NEH = seq_NEH2.copy()
        
    return seq_NEH


'''
Fonctions pour la résolution par évaluation et séparation
'''

################################################################################
# exo 4 :
################################################################################
def date_dispo(machine, job):
    ''' Renvoie la valeur de r_kj avec k = 'machine' et j = 'job
    '''

    if machine == 0:
        return 0
    
    return sum(job['durée'][:machine]) # machine exclus



# calcul de q_kj
def duree_latence(machine, job, nombre_machines):
    ''' Renvoie la valeur de q_kj avec k = 'machine' et j = 'job
    '''

    if machine == nombre_machines - 1:
        return 0
    
    return sum(job['durée'][machine+1:]) # machine exclus


# calcul de la somme des durées des opérations d'une liste
# exécutées sur une machine donnée
def duree_jobs(machine, liste_jobs):
    ''' Renvoie la somme des durées des opérations sur 'machine' des jobs de 
        'liste_jobs'
    '''
    durée = 0
    for job in liste_jobs:
        durée += job['durée'][machine]

    return durée


################################################################################
# exo 5 :
################################################################################

def makespan_probleme_1_rj_cmax(dates_au_plus_tot, durées_jobs): 
    '''
    Fonction annexe qui renvoie le makespan pour le problème 1|rj|Cmax
    Utilisée dans la fonction eval
    '''
    if dates_au_plus_tot.__len__ == 0 or durées_jobs.__len__ == 0:
        return -1
    
    makespan = 0
    for i in range(len(durées_jobs)):

        if makespan >= dates_au_plus_tot[i]:    # pas besoin d'attendre
            makespan += durées_jobs[i]
        else:                                   # il faut attendre
            makespan = dates_au_plus_tot[i] + durées_jobs[i]

    return makespan



def eval(ordo, liste_jobs):
    ''' Renvoie la valeur du minorant en tenant compte de l'ordonnancement 
        'ordo' et des jobs non places de liste_jobs
    '''
    nb_machines = len(ordo['disponibilité'])

    ############## Version bizarre qui marche ####################
    # LB2 = []
    
    # for machine in range(nb_machines):
    #     min_qj = min([duree_latence(machine, job, nb_machines) for job in liste_jobs])
    #     LB2.append(ordo['disponibilité'][machine] + min_qj)    
    
    # return max(LB2)

    ############## Version du cours longue ####################
    # LB = []
    # for machine in range(nb_machines):
    #     LB.append(
    #               min([date_dispo(machine, job) for job in liste_jobs]) + 
    #               sum([job['durée'][machine] for job in liste_jobs]) + 
    #               min([duree_latence(machine, job, nb_machines) for job in liste_jobs]) )

    # return  ordo['disponibilité'][0] + max(LB)



    ############## Version avec LB2 (voir papier scientifique indiqué dans le TP) ####################


    if liste_jobs.__len__==0:
        return ordo['diponibilité'][nb_machines-1]

    LB2 = []
    for machine in range(nb_machines):
        dates_au_plus_tot_jobs = sorted([ (date_dispo(machine, job), idx, job) for idx, job in enumerate(liste_jobs)])

        # print(dates_au_plus_tot_jobs)
        dates_au_plus_tot, _, jobs = list(zip(*dates_au_plus_tot_jobs))
        # print(dates_au_plus_tot, [job['durée'] for job in jobs])
        makespan = makespan_probleme_1_rj_cmax(dates_au_plus_tot, [job['durée'][machine] for job in jobs])

        dates_de_latence = [duree_latence(machine, job, nb_machines) for job in liste_jobs]

        LB2.append(makespan + min(dates_de_latence))

    return ordo['disponibilité'][0] + max(LB2)

def creer_sommet(evaluation, places, non_places, numero):
    # liste des jobs déjà placés
    return  (evaluation,
            numero,
            places,
            non_places
            )

################################################################################
# exo 6 :
################################################################################
def evaluation_separation(flowshop):
    ''' Résout par évaluation et séparation le problème défini par 
        'flowshop'
    '''

    nb_machines = flowshop['nombre machines']

    # calcul d'une borne supérieure initiale par l'algo NEH
    l_NEH = liste_NEH(flowshop)

    ordo = creer_ordo_vide(nb_machines)
    ordonnancer_liste_jobs(ordo, l_NEH)
    val_solution = ordo['disponibilité'][nb_machines-1]

    print("Valeur solution de départ =", val_solution)
    liste_solution = l_NEH.copy()

    arbre = []  # utilisé sous forme de file de priorité avec heapq
    evaluation = eval(ordo, l_NEH)

    # création de la racine
    numero = 1
    s = creer_sommet(evaluation, [], l_NEH, numero)
    # qui est ajouté à la file de priorité
    heapq.heappush(arbre, s)

    while arbre != []:
        evaluation, _numero, places, non_places = heapq.heappop(arbre)

        # Séparation
        for i in range(len(places)+1): # on crée un sommet pour chaque nouvel ordonnancement
            new_places = places[:i] + [non_places[0]] + places[i:]
            new_ordo = creer_ordo_vide(nb_machines)
            ordonnancer_liste_jobs(new_ordo, new_places)
            new_non_places = non_places[1:]
            

            if new_non_places.__len__() == 0: # évalutation

                ordo = creer_ordo_vide(nb_machines)
                ordonnancer_liste_jobs(ordo, new_places)
                durée_ordo = ordo['disponibilité'][nb_machines-1]

                if durée_ordo < val_solution:
                    print(f"Amélioration trouvée, {durée_ordo=} {evaluation=}")
                    val_solution = durée_ordo
                    liste_solution = new_places.copy()
                    continue
            
            else:
                new_eval = eval(new_ordo, new_non_places)
                if new_eval <= val_solution:
                    numero += 1
                    s = creer_sommet(new_eval, new_places, new_non_places, numero)
                    heapq.heappush(arbre, s)

    return val_solution, liste_solution, numero