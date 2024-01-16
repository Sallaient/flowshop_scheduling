import genetique
import flowshop as fl

path = "tai11-1582.txt"
genetique.genetique_from_file(path, pop_size=100, taux_mutation=0.1, nb_iterations=1000)
# list neh
# flowshop = fl.lire_flowshop(path)
# list_neh = fl.liste_NEH(flowshop)
# ordo = fl.creer_ordo_liste_jobs(flowshop['nombre machines'],list_neh)
# fl.afficher_ordo(ordo)