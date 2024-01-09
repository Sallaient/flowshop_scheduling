import recuit_simule
import flowshop


if __name__ == "__main__":

    # solution_init = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # print(sol_voisine(solution_init))

    # fs = flowshop.lire_flowshop("jeu4-844.txt")
    # l_NEH = flowshop.liste_NEH(fs)
    
    # print(recuit_simule(l_NEH, fs['nombre machines'], max_iter=1e5, temp_init=1e6))

    # fs_path = "jeu2-704.txt"
    # fs_path = "jeu3-973.txt"
    fs_path = "jeu4-844.txt"
    recuit_simule.erreur(fs_path, max_iter=1e5, temp_init=1e6, nb_iter=10)

    # fs = flowshop.lire_flowshop("jeu3-973.txt")

    # l_NEH = flowshop.liste_NEH(fs)

    # liste_sol = recuit_simule.recuit_simule(l_NEH, fs['nombre machines'], max_iter=1e5, temp_init=1e6)
    # print(liste_sol)