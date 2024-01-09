import recuit_simule
import flowshop


if __name__ == "__main__":
    # fs_path = "jeu2-704.txt"
    # fs_path = "jeu3-973.txt"
    fs_path = "jeu4-844.txt"
    recuit_simule.erreur(fs_path, max_iter=1e5, temp_init=1e6, nb_iter=10)

