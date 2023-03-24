from PLUS_classe_joeuur import *

def creer_joueur(nb_joueurs : int, l_nom_joueurs : list, id_IA : int, IA_Diamant):
    """
    Principe :
        Il crée un à un les objets joueurs
    Entrée :
        nb_joueur           [INT]   : Nombre de joueurs en jeu
        l_nom_joueurs       [LIST]  : Les noms de chaque joueurs
        id_IA               [INT]   : Numéro de l'IA parmis les joueurs
    Sortie :
        l_joueurs           [LIST]  : Liste des objets joueurs
    """

    l_joueurs = []

    for joueur_a_creer in range(nb_joueurs):
        if joueur_a_creer == id_IA:
            l_joueurs.append(Joueur_X8(joueur_a_creer,l_nom_joueurs[joueur_a_creer], True))  # On crée l'objet joueur représentant l'IA
        else:
            l_joueurs.append(Joueur_X8(joueur_a_creer, l_nom_joueurs[joueur_a_creer], False))

        l_joueurs[len(l_joueurs) - 1].init_historique(IA_Diamant)

    return l_joueurs
