"""
Permet de tester l'IA un grand nombre de fois et de l'améliorer


Basé sur l'algorithme qu'avait fait le vidéaste Laupok sur YouTube.

"""

from random import *
from datetime import datetime
import pickle
import time
import math
from moteur_diamant import *
# from moteur_diamant_V2 import *
from IA.IA_Picsou import *

itteration_bcl = 0


nbInnovation = 0
NB_INPUT = 7  # Nombre de neurones d'entrée
NB_OUTPUT = 2  # Nombre de neurones de sortie
# NB_INDIVIDU_POPULATION = 8  # Nombre d'individus au sein d'une population
NB_NEURONE_MAX = 1000
anciennes_populations = []  # Liste les anciennes populations
maxscore = 0  # Le meilleur score d'un individu sur toute les générations

# Pour les mutations
CHANCE_MUTATION_RESET_CONNEXION = 0.25
POIDS_CONNEXION_MUTATION_AJOUT = 0.8
CHANCE_MUTATION_POIDS = 0.75  # Probabilité qu'on mute les poids des connexions

CHANCE_MUTATION_CONNEXION = 0.85  # Probabilité qu'on ajoute une connexion entre deux neurones
CHANCE_MUTATION_NEURONE = 0.69  # Probabilité qu'on ajoute un neurone à une connexion

# Pour calculer les différences entre individu et trier la population par espèces
EXCES_COEF = 0.5
POIDSDIFF_COEF = 0.92
DIFF_LIMITE = 1

# Pour les sauvegardes
CHEMIN_SAVE_HISTORIQUE_POPULATIONS = "save_pickle/HISTORIQUE_POPULATIONS/"  # Sauvegarde chaque population avec l'horodatage actuel
CHEMIN_SAVE_ANCIENNES_POPULATIONS = "save_pickle/ANCIENNES_POPULATIONS/"  # Sauvegarde bêtement la liste des anciennes populations
CHEMIN_SAVE_INDIVIDU_PLUS_FORT = "save_pickle/"  # Si on trouve un individu plus fort, on remplace l'ancien
CHEMIN_SAVE_INFO_TEMPS_REEL = "save_pickle/INFO_TEMPS_REEL/"  # Sauvegarde les informations affichées en temps réel dans le terminal
CHEMIN_SAVE_RAPPORT = "save_pickle/"  # Récapitule les actions passées
RAPPORT = [">>>> Début du rapport"]  # Contient les lignes du rapport
DIRECT_CONSOLE = []  # Affichage des infos d'où on est le générateur dans la console

# CHEMIN_SAVE_ONEDRIVE = "D:/Logiciel/OneDrive/OneDrive - ens.uvsq.fr/SAE_IA/Generateur_vers_OneDrive/"
CHEMIN_SAVE_ONEDRIVE = "save_pickle/test/"
DERNIER_SAUVEGARDE_ONEDRIVE = None


def clearConsole():
    print("\n" * 10)


def genererNombreDeJoueurs():
    # return randint(3, 10)

    return 4


def genererPoids():
    """
    Principe :
        Génère un poids, 50% de chance que ce soit 1, 50% de chance que ce soit -1.
    Sortie :
        Le poids
    """

    # return 1 if randint(0, 1) == 0 else -1
    return 1 if randint(0, 1) else -1


class LESANCIENSMEILLEURS:
    #  On garde en mémoire les deux derniers meilleurs individus et leur espèce.
    def __init__(self):
        # On initialise
        self.inieme_individu = 0
        self.meilleur_espece = None
        self.meilleur_individu = None
        self.ratio_ardoise = 0  # TotalDiamantsDesJoueurs / 4 ||||| Plus c'est haut, plus c'est woaw

        self.__ancien_meilleur_espece = None
        self.__ancien_meilleur_individu = None
        self.__ancien_ratio_ardoise = 0

    def nouveau_meilleur(self, nouvel_espece, nouvel_individu, ratio_ardoise):
        assert type(nouvel_espece) == ESPECE
        assert type(nouvel_individu) == INDIVIDU

        if self.inieme_individu == 0:
            # Si c'est le premier meilleur
            self.meilleur_espece = nouvel_espece
            self.meilleur_individu = nouvel_individu
        else:
            # S'il doit remplacer un meilleur
            self.__ancien_meilleur_espece = self.meilleur_espece
            self.__ancien_meilleur_individu = self.meilleur_individu
            self.__ancien_ratio_ardoise = self.ratio_ardoise

            self.inieme_individu += 1
            self.meilleur_espece = nouvel_espece
            self.meilleur_individu = nouvel_individu
            self.ratio_ardoise = ratio_ardoise


class Info_IA:
    def __init__(self):
        self.no_generation = 0  #
        self.nb_espece = 0  #
        self.temps_boucle = ""
        self.meilleur_score = 0
        self.score_moyen_espece = 0
        self.len_liste_connexions = 0
        self.len_liste_neurones = 0
        self.id_espece_du_meilleur = 0
        self.meilleur_score_fin_partie = 0

    def retourne_liste_info(self):
        msg = [
            "=============================================================",
            "Temps depuis le lancement du générateur : " + str(self.temps_boucle),
            "---",
            "No génération : " + str(self.no_generation),
            "Nb Espèces : " + str(self.nb_espece),
            "Le score du meilleur joueur à la fin de la partie EN COMPTANT LES MALUS: " + str(
                self.meilleur_score_fin_partie),
            "---",
            "Score du meilleur individu : " + str(self.meilleur_score),
            "Identifiant de son espèce :" + str(self.nb_espece),
            "Score moyen de son espèce : " + str(self.score_moyen_espece),
            "---",
            "Nombre de neurones de l'individu : " + str(self.len_liste_neurones),
            "Nombre de connexions de l'individu :" + str(self.len_liste_connexions),
            "============================================================="
        ]
        return msg



objet_info = Info_IA


class NEURONE:
    # Créer un neurone vide
    # Note : Inspiré du travail du vidéaste Laupok.

    def __init__(self):
        self.valeur = 0  # Valeur du neurone par défaut
        self.id = -1  # Id par défaut d'un neurone créer (devra être changé).
        self.typeNeurone = ""  # Type de neurone (INPUT, OUTPUT, CACHER)

    def copier(self, neurone_a_copier: NEURONE):
        self.valeur = neurone_a_copier.valeur
        self.id = neurone_a_copier.id
        self.typeNeurone = neurone_a_copier.typeNeurone


class CONNEXION:
    def __init__(self):
        self.innovation = 0  # Identifiant unique de la connexion. Indique que c'est l'innovation ème connexion.
        self.entree = 0  # Neurone d'entrée
        self.sortie = 0  # Neurone de sortie
        self.actif = True  # Le neurone est actif ou mort
        self.poids = 0  # Poids de la connexion

    def copier(self, connexion_a_copier: CONNEXION):
        assert type(connexion_a_copier) == CONNEXION, "ce n'est pas un individu"

        self.innovation = connexion_a_copier.innovation
        self.entree = connexion_a_copier.entree
        self.sortie = connexion_a_copier.sortie
        self.actif = connexion_a_copier.actif
        self.poids = connexion_a_copier.poids


class INDIVIDU:
    # Créer un individu vide, c'est-à-dire un réseau de neurone de base.
    # Note : Inspiré du travail du vidéaste Laupok.
    def __init__(self):
        self.idEspece = 0  # Identifiant de l'espèce où appartient l'individu
        self.nbNeurones = 0  # Le nombre de neurones qui composent l'individu (le réseau de neurones).
        # en dehors des neurones d'entrées (INPUT) et de sorties (OUTPUT).
        self.score = 1  # Score qu'a fait l'individu (nombre de diamants +1 de gagné)
        self.lesNeurones = []  # Liste de tous les neurones de l'individu
        self.lesConnexions = []  # Liste les connexions entre les neurones de l'individu.

        self.nbInnovationConnexions = 0

    def copier(self, individu_a_copier):
        assert type(individu_a_copier) == INDIVIDU, "ce n'est pas un individu"

        self.idEspece = individu_a_copier.idEspece
        self.nbNeurones = individu_a_copier.nbNeurones
        self.score = individu_a_copier.score

        # On copie la liste de neurones
        self.lesNeurones = []
        for neurone_a_copier in individu_a_copier.lesNeurones:
            neurone_cree = creer_neurone()
            neurone_cree.copier(neurone_a_copier)

            self.lesNeurones.append(neurone_cree)

        # On copie la liste de connexions
        self.lesConnexions = []
        for connexion_a_copier in individu_a_copier.lesConnexions:
            connexion_cree = creer_connexion()
            # print("hellooooooooooooooooo")
            connexion_cree.copier(connexion_a_copier)

            self.lesConnexions.append(connexion_cree)
            # print("ooooo", self.lesConnexions)

        self.nbInnovationConnexions = individu_a_copier.nbInnovationConnexions


class ESPECE:
    def __init__(self):
        self.nbEnfants = 0  # Nombre d'individus enfants qu'a faits l'espèce
        self.scoreMoyen = 0  # Nombre moyen de diamants que récolte l'espèce par parties
        self.scoreMax = 0  # Nombre maximum de diamants qu'a fait un individu de l'espèce.
        self.lesIndividus = []  # Liste des objets individus


def creer_neurone(): return NEURONE()


def creer_connexion(): return CONNEXION()


def creer_individu():
    individu = INDIVIDU()

    for id_neurone_input in range(NB_INPUT):
        ajouter_neurone(individu, id_neurone_input, "INPUT", 0)

    for id_neurone_output in range(NB_INPUT, NB_INPUT + NB_OUTPUT):
        ajouter_neurone(individu, id_neurone_output, "OUTPUT", 0)

    return individu


def creer_espece(): return ESPECE()


def creer_population(nb_joueurs=genererNombreDeJoueurs()):
    """
    Principe :
        Une population comporte des individus. Ces individus sont des réseaux de neurones.
        Une nouvelle génération est une nouvelle population baser sur la population précédente (l'ancienne génération).

        Ici, on initialise juste une population avec des individus vide
    Entrée :
        Rien
    Sortie :
        population      [LIST] : Liste d'objet individu (réseau de neurones).
    """

    population = [creer_individu() for _ in range(nb_joueurs)]

    return population


def ajouter_neurone(individu, id_neurone, typeNeurone, valeur):
    """
    Principe :
        Ajoute un neurone à un individu (réseau de neurone).
    Entrée :
        individu        [INDIVIDU] : Un réseau de neurone
        id                   [INT] : Identifiant du neurone dans le réseau
        typeNeurone         [STR] : Type de neurone : INPUT, OUTPUT, CACHER
        valeur               [INT] : Valeur du neurone
    Sortie :
        Aucune, on met juste à jour l'objet.
    """
    assert type(individu) == INDIVIDU, "ERREUR > Ce n'est pas un individu"
    assert id_neurone >= 0, "ERREUR > id doit commencer par 0"
    assert typeNeurone in ["INPUT", "OUTPUT", "CACHER"], "ERREUR > Type d'individu invalide"
    assert type(valeur) == int, "ERREUR > Type invalide"

    neurone = creer_neurone()
    neurone.id = id_neurone
    neurone.typeNeurone = typeNeurone
    neurone.valeur = valeur

    individu.lesNeurones.append(neurone)


def ajouter_connexion(individu, id_neurone_entree, id_neurone_sortie):
    """
    Principe :
        Ajoute une connexion entre deux réseaux de neurones
    Entrée :
        individu            [INDIVIDU] : Réseau de neurone
        id_neurone_entree       [INT] : Neurone d'entrée  (celui à gauche)
        id_neurone_sortie       [INT] : Neurone de sortie (celui à droite)
    Sortie :
        Rien, modifie juste la liste lesConnexions de l'individu
    """
    global nbInnovation

    connexion = creer_connexion()  # On crée un objet connexion vide
    connexion.actif = True  # On dit que la connexion est fonctionnelle
    connexion.entree = id_neurone_entree  # On indique le neurone d'entrée
    connexion.sortie = id_neurone_sortie  # On indique le neurone de sortie
    connexion.poids = genererPoids()  # On génère un poids aléatoire pour la connexion
    connexion.innovation = nbInnovation  # On indique que c'est la combientième innovation.

    individu.lesConnexions.append(connexion)
    nbInnovation += 1


def mutationPoidsConnexions(individu):
    """
    Principe :
        On mute les poids des connexions
        
        Soit on reset le poids, soit on la modifie.
    Entrée :
        individu        [INDIVIDU] : Réseau de neurones
    """
    assert type(individu) == INDIVIDU, "erreur ce n'est pas un individu"

    for connexion in individu.lesConnexions:
        if connexion.actif:
            if random() < CHANCE_MUTATION_RESET_CONNEXION:
                connexion.poids = genererPoids()
            else:
                if random() >= 0.5:
                    connexion.poids -= POIDS_CONNEXION_MUTATION_AJOUT
                else:
                    connexion.poids += POIDS_CONNEXION_MUTATION_AJOUT


def mutationAjouterConnexion(individu):
    """
    Principe :
        Créer si possible, une connexion entre deux neurones
    Entrée :
        individu        [INDIVIDU] : Réseau de neurone
    """

    liste_melanger = individu.lesNeurones.copy()
    shuffle(liste_melanger)  # On mélange la liste

    on_a_creer_une_connexion = False  # Tant qu'on a pas créé de connexion, c'est False

    neuroneA = 0  # Numéro du 1er neurone qu'on teste.
    neuroneB = 0  # Numéro du second neurone qu'on teste.

    while neuroneA < len(individu.lesNeurones) and not on_a_creer_une_connexion:
        while neuroneB < len(individu.lesNeurones) and not on_a_creer_une_connexion:
            if neuroneA != neuroneB:

                possible = False

                # On vérifie qu'une connexion est plausible.
                # Rappel : INPUT → Neurone d'entrée / OUTPUT → Neurone de sortie / CACHER → Neurone caché

                couple = [individu.lesNeurones[neuroneA].typeNeurone, individu.lesNeurones[neuroneB].typeNeurone]
                possible = True if couple == ["INPUT", "OUTPUT"] else possible
                possible = True if couple == ["CACHER", "CACHER"] else possible
                possible = True if couple == ["CACHER", "OUTPUT"] else possible

                # if couple != ['INPUT', 'INPUT']:
                #    print("couple ===>", couple)
                #    print("            ", possible)

                if possible:

                    toujours_possible = True  # On initialise comme si c'est toujours possible de créer une connexion
                    test_connexion_id = 0

                    # On teste si une connexion entre le neuroneA et le neuroneB n'existe pas déjà
                    while test_connexion_id < len(individu.lesConnexions) and toujours_possible:
                        test_connexion = individu.lesConnexions[test_connexion_id]
                        if test_connexion.actif:
                            if test_connexion.entree == neuroneA and test_connexion.sortie == neuroneB:
                                toujours_possible = False  # Une connexion du même type existe déjà

                        test_connexion_id += 1

                    # La connexion entre le neuroneA et le neuroneB est inédite, on peut la faire !

                    if toujours_possible:
                        ajouter_connexion(individu, neuroneA, neuroneB)
                        on_a_creer_une_connexion = True
                        # print("----> On a créer une connexion")

            neuroneB += 1

        neuroneA += 1


def mutationAjouterNeurone(individu):
    """
    Principe :
        On ajoute un neurone sur une connexion.
        Donc la connexion se désactive pour laisser place à 2 connexions reliant le neurone A au nouveau neurone.
        Mais également le nouveau neurone au neurone B.
    Entrée :
        individu        [INDIVIDU] : Réseau de neurone
    """

    if len(individu.lesConnexions) <= 0:
        # S'il n'y a pas de connexion
        return
    if len(individu.lesNeurones) >= NB_NEURONE_MAX:
        # Si on a dépassé le maximum de neurone possible
        return

    liste_melanger = individu.lesConnexions.copy()
    shuffle(liste_melanger)  # On mélange la liste

    id_liste_melanger = 0
    on_a_creer_un_neurone = False
    while id_liste_melanger < len(
            liste_melanger) and not on_a_creer_un_neurone:  # Tant qu'on a pas terminé la liste et pas créer de neurone
        connexion = liste_melanger[id_liste_melanger]  # On récupère l'objet connexion choisit

        if connexion.actif:  # Si la connexion est fonctionnelle (on ne place pas de neurone sur une connexion obsolète...)
            connexion.actif = False

            id_nouveau_neurone = NB_INPUT + NB_OUTPUT + individu.nbNeurones  # RAPPEL : l'identifiant du tout premier neurone est 0.
            individu.nbNeurones += 1  # On compte qu'on a ajouté un neurone caché au réseau

            ajouter_neurone(individu, id_nouveau_neurone, "CACHER", 1)

            # Exemple :
            # Ancienne connexion : A --- B (1 connexion représenté par ---)
            # Nouveau neurone : Z
            # Alors : A --- Z --- B (2 nouvelles connexions)
            ajouter_connexion(individu, connexion.entree, id_nouveau_neurone)
            ajouter_connexion(individu, id_nouveau_neurone, connexion.sortie)

            on_a_creer_un_neurone = True

        id_liste_melanger += 1  # On passe à la connexion suivante


def mutation(individu):
    """
    Principe :
        On tire un nombre au hasard et on fait 3 comparaisons pour voir si :
            - on mute le poids des connexions
            - on ajoute une connexion
            - on ajoute un neurone.

    Entrée :
        individu [INDIVIDU]     : Réseau de neurone
    """
    assert type(individu) == INDIVIDU

    nb_aleatoire = random()
    # print(nb_aleatoire)
    if nb_aleatoire < CHANCE_MUTATION_POIDS:
        mutationPoidsConnexions(individu)
    if nb_aleatoire < CHANCE_MUTATION_CONNEXION:
        # print("creer connnexion")
        mutationAjouterConnexion(individu)
    if nb_aleatoire < CHANCE_MUTATION_NEURONE:
        # print("patage")
        mutationAjouterNeurone(individu)


def getDisjoint(unIndividuA: INDIVIDU, unIndividuB: INDIVIDU):
    """
    P :
        Compte le nombre de connexions qui ne sont pas en commun.

        Deux connexions sont en commun si elles ont la même innovation.
        Chaque connexion possède une innovation unique.
        Si deux connexions possèdent la même innovation, c'est que les individus viennent
        de la même famille. Ils ont donc pu hériter de la même connexion.

        A noté que les poids des connexions peuvent être différent
    E :
        unIndividuA     INDIVIDU : Un réseau de neurone A
        unIndividuB     INDIVIDU : Un réseau de neurone B
    S :
        nb_diff_connexion    INT : Nombre de connexions différentes
    """

    nb_diff_connexion = 0

    for connexionA in unIndividuA.lesConnexions:
        for connexionB in unIndividuB.lesConnexions:
            if connexionA.innovation != connexionB.innovation:  # Si on a deux même connexion
                nb_diff_connexion += 1

    return nb_diff_connexion


def getDiffPoids(unIndividuA: INDIVIDU, unIndividuB: INDIVIDU):
    """
    P :
        Compte le total de différences entre les poids d'une même connexion.

        Donc on regarde que si même si elles étaient à l'époque une et unique connexion,
        elles restent similaires.
        Puis on fait une moyenne du poids d'une connexion en commun
    E :
        unIndividuA     INDIVIDU : Un réseau de neurone A
        unIndividuB     INDIVIDU : Un réseau de neurone B
    S :
       INT : moyenne du poids d'une connexion en commun.
    """
    nb_meme_connexion = 0
    total_poids = 0

    for connexionA in unIndividuA.lesConnexions:
        for connexionB in unIndividuB.lesConnexions:
            if connexionA.innovation == connexionB.innovation:
                nb_meme_connexion += 1
                total_poids = abs(connexionA.poids + connexionB.poids)

    if nb_meme_connexion == 0:  # Elles n'ont aucune connexion en commun, alors on renvoie un nombre tel pour les différencier.
        return 999999
    else:
        return total_poids / nb_meme_connexion  # Moyenne du poids d'une connexion en commun


def tauxDeDifference(ind_a_trier, ind_rep):
    """
    P :
        Estime la différence entre les deux individus.
        Plus ils sont différents, plus le nombre renvoyé est élevé
    E :
        ind_a_trier         INDIVIDU : Individu qui doit être trié
        ind_rep             INDIVIDU : Individu qui représente son espèce
    S :
        taux_diff           INT      : Taux de différence entre les deux individus.
    """

    A = (EXCES_COEF * getDisjoint(ind_a_trier,
                                  ind_rep))  # Plus ce nombre est élevé, plus les connexions sont totalement différentes.
    B = (max(len(ind_a_trier.lesConnexions) + len(ind_rep.lesConnexions),
             1))  # Total du nombre de connexions, 1 s'ils n'en n'ont pas.
    C = POIDSDIFF_COEF * getDiffPoids(ind_a_trier,
                                      ind_rep)  # Plus ce nombre est élevé, plus les connexions similaires sont différentes.

    return A / B + C  # Taux de différence entre les deux individus


def trierPopulation(laPopulation):
    """
    P :
        On trie les individus par espèce.
        On prend le dernier individu, et on crée une espèce avec.
        Puis on choisit un individu parmi cette espèce, et on compare.
            → Si c'est proche, on l'ajoute à l'espèce
            → si c'est trop différent, on lui crée une espèce
    E :
        laPopulation        LIST : liste d'individus dans la population
    S :
        lesEspeces          LIST : Liste les espèces
    """

    lesEspeces = [creer_espece()]  # On crée une espèce
    lesEspeces[0].lesIndividus.append(
        laPopulation[len(laPopulation) - 1])  # On place le dernier individu dans cet espèce

    for id_individu_select in range(len(laPopulation) - 1):  # On sélectionne un individu à trier
        trouve = False  # On marque qu'on a pas trouvé d'espèce
        id_espece = 0
        while id_espece < len(
                lesEspeces) and trouve == False:  # Tant qu'on est dans la liste et qu'on a pas trouvé d'espèce.
            espece = lesEspeces[id_espece]
            individu_select = laPopulation[id_individu_select]

            nb_aleatoire = randint(0, len(espece.lesIndividus) - 1)  # On tire un individu aléatoirement
            representant_espece = espece.lesIndividus[nb_aleatoire]  # On le définit comme représentant de l'espèce

            taux_de_difference = tauxDeDifference(individu_select, representant_espece)

            if taux_de_difference < DIFF_LIMITE:  # Si True, alors il a assez de similitude pour intégrer l'espèce
                individu_select.idEspece = id_espece
                espece.lesIndividus.append(individu_select)
                trouve = True  # On l'a mis dans une espèce

            id_espece += 1  # On passe à l'espèce suivante

        if not trouve:
            lesEspeces.append(creer_espece())

            laPopulation[id_individu_select].idEspece = len(lesEspeces) - 1
            lesEspeces[len(lesEspeces) - 1].lesIndividus.append(laPopulation[id_individu_select])
            j = lesEspeces[len(lesEspeces) - 1].lesIndividus

    return lesEspeces


def trierEspecesParScoreMoyen(lesEspeces):
    """
    P :
        Note : Cette fonction n'est pas présente dans lesEspecesTrier'algorithme de Laupok.

        On trie les espèces en fonction de leur scoreMax.
        L'espèce avec le plus grand scoreMax sera en premier, celui avec le plus petit sera en dernier.

        Algorithme utilisé : trie sélectif (d'après le cours)
    E :
        lesEspeces          LISTE : Liste ses espèces
    S :
        lesEspecesTrier     LISTE : Liste des espèces, mais trié.
    """

    lesEspecesTrier = lesEspeces.copy()

    for i in range(len(lesEspecesTrier)):
        # On parcourt normalement le tableau avec un pointeur i

        # Remarque :
        # Laupok utilise la fonction table.sort (en langage LUA).
        # Il trie en fonction du fitnessMax (scoreMax) des espèces.
        # Sauf que pour Diamants, un individu a pu avoir plus de diamants par chance.
        # Utiliser la moyenne est plus sûr.

        minimum = lesEspecesTrier[i].scoreMoyen
        pointeur_min = i
        for j in range(i + 1, len(lesEspecesTrier)):
            # On parcourt à partir de cette valeur. Mais on garde le pointeur i sur la valeur de départ.
            # Le pointeur j se déplace.
            if lesEspecesTrier[j].scoreMoyen < minimum:
                # On a trouvé une plus petite valeur
                minimum = lesEspecesTrier[j].scoreMoyen
                pointeur_min = j

        lesEspecesTrier[i], lesEspecesTrier[pointeur_min] = lesEspecesTrier[pointeur_min], lesEspecesTrier[
            i]  # On échange la valeur de départ avec la plus petite valeur trouvé après.

    return lesEspecesTrier


def crossover(unIndividuA: INDIVIDU, unIndividuB: INDIVIDU):
    """
    P :
        Retourne un mélange entre les deux réseaux de neurones.
    E :
        unIndividuA, unIndividuB        INDIVIDU : Un réseau de neurone
    S :
        individuEnfant                 INDIVIDU : L'individu issu de ce crossover
    """

    # On initialise un individu enfant vierge
    individuEnfant = creer_individu()

    # On désigne qui est le meilleur individu, et qui est le moins bon
    if unIndividuA.score < unIndividuB.score:
        leNul = unIndividuA
        leBon = unIndividuB
    else:
        leNul = unIndividuB
        leBon = unIndividuA

    # L'individu enfant se base sur le meilleur individu parent
    individuEnfant.copier(leBon)

    # Cependant, il hérite aussi du moins bon individu parent

    for connexionEnfant in individuEnfant.lesConnexions:
        id_connexionNul = 0
        a_ete_copier = False  # True si on vient de lui copier une connexionNul

        while id_connexionNul < len(leNul.lesConnexions) and not a_ete_copier:
            connexionNul = leNul.lesConnexions[id_connexionNul]

            if connexionEnfant.innovation == connexionNul.innovation and connexionNul.actif:
                if random() > 0.5:
                    connexionEnfant.copier(connexionNul)

                    assert connexionNul != connexionEnfant, "il y a un problème : même objet......"
                    a_ete_copier = True

            id_connexionNul += 1

    individuEnfant.score = 1
    return individuEnfant


def choisirParent(uneEspece):
    """
    P :
        Renvoie une copie d'un parent choisit dans une espèce
    E :
        uneEspece       ESPECE : Une espèce
    S :
        INDIVIDU : l'individu parent
    """

    if len(uneEspece) == 1:
        return uneEspece[0]

    scoreTotal = 0

    for individu in uneEspece:
        scoreTotal += individu.score

    limite = randint(0, scoreTotal)
    total = 0

    for individu in uneEspece:
        total += individu.score

        if total >= limite:
            # Si la somme des scores cumulés dépasse total, on renvoie l'individu qui a fait dépasser la limite.
            return individu

    assert 1 == 2, "impossible de trouver un parent ?"


def nouvelleGeneration(laPopulation, lesEspeces, lesAnciensMeilleurs_X8, grille_victoire_fin_partie=[], joueurs=[]):
    """
    P :
        À partir de la population précédemment créer, plus sa version triée, on détermine le nombre de bébés que peut
        faire chaque espèce.
        Plus son score moyen (nombre de diamants récupéré en moyenne) est haut,
        plus l’espèce a le droit de faire des bébés.
        Si elle ne fait pas de bébé, alors elle est éliminée à cause de la sélection naturelle.
    E :
        laPopulation    LIST : Liste des individus au sein d'une population
        lesEspeces      LIST : Liste les espèces en jeu
    S :
        laNouvellePopulation    LIST : Liste des individus au sein de la nouvelle population
    """

    NB_INDIVIDU_POPULATION = genererNombreDeJoueurs()
    nbIndividuACreer = NB_INDIVIDU_POPULATION
    indiceNouvelleEspece = 0

    # On initialise la nouvelle population.
    laNouvellePopulation = []

    # On vérifie que le meilleur individu de la population soit bien le meilleur individu
    # depuis le tout début.
    # Il peut y avoir une mauvaise mutation, et dans ce cas-là, nos résultats sont mauvais.
    # Donc on doit corriger ce problème.

    #################

    # print("====uiop")

    # print('jalabet', grille_victoire_fin_partie)
    if grille_victoire_fin_partie:
        # print('wolla')
        for id_joueur in range(len(joueurs)):
            joueur = joueurs[id_joueur].Picsou_objet_joueur_X8

            if grille_victoire_fin_partie[id_joueur] < 0:
                # On réajuste

                grille_victoire_fin_partie[id_joueur] = 0

            # On met à jour son score
            laPopulation[id_joueur].score = grille_victoire_fin_partie[id_joueur] + 1

        maxNbDiamantsJoueurs = max(grille_victoire_fin_partie)
        totalNbDiamantsJoueurs = sum(grille_victoire_fin_partie)
        nbJoueurs = genererNombreDeJoueurs()

        ratio_ardoise_population = totalNbDiamantsJoueurs / nbJoueurs  # Plus c'est grand, plus ça signifie que la partie était corsé (donc intéressante)

        #print("yoooooo", ratio_ardoise_population, lesAnciensMeilleurs_X8.ratio_ardoise)

        if (ratio_ardoise_population > lesAnciensMeilleurs_X8.ratio_ardoise and ratio_ardoise_population > 50 and maxNbDiamantsJoueurs < 130 and maxNbDiamantsJoueurs > 50) or lesAnciensMeilleurs_X8.meilleur_individu is None:
            # print("====kjh")
            # Si on a fait un meilleur ratio, alors cela signifie que cette partie a été compliqué pour l'IA, mais
            # qu'elle a réussi à s'en sortir.

            PlusFort = creer_individu()

            # on récupère le meilleur joueur
            maximum_nbdiamants = grille_victoire_fin_partie[0]
            id_maximum_nbdiamants = 0
            for id_joueur in range(len(grille_victoire_fin_partie)):
                if maximum_nbdiamants < grille_victoire_fin_partie[id_joueur]:
                    maximum_nbdiamants = grille_victoire_fin_partie[id_joueur]
                    id_maximum_nbdiamants = id_joueur

            # On le désigne comme le meilleur
            PlusFort.copier(laPopulation[id_maximum_nbdiamants])

            lesAnciensMeilleurs_X8.nouveau_meilleur(lesEspeces[PlusFort.idEspece], PlusFort, ratio_ardoise_population)
            lesAnciensMeilleurs_X8.inieme_individu += 1

        elif randint(1,5) == 1:
            # print('dfg')
            # On initialise comme étant le meilleur

            for espece in lesEspeces:
                for id_individu in range(len(espece.lesIndividus)):
                    # On remplace tout le monde par l'ancien meilleur individu.
                    # Comme ça, on est sûr que le meilleur domine totalement.

                    #print(type(lesAnciensMeilleurs_X8.meilleur_individu))
                    espece.lesIndividus[id_individu].copier(lesAnciensMeilleurs_X8.meilleur_individu)
                    assert espece.lesIndividus[id_individu].score == lesAnciensMeilleurs_X8.meilleur_individu.score


    ################

    """
    scoreMaxPop = 0
    PlusFort = creer_individu()
    scoreMaxAncPop = 0
    ancienPlusFort = creer_individu()
    
    # On prend le score du meilleur individu de la population.
    for individu in laPopulation:
        if scoreMaxPop < individu.score:
            scoreMaxPop = individu.score
            PlusFort = individu  # On le garde en mémoire comme quoi c'est le meilleur individu

    if lesAnciensMeilleurs_X8.inieme_individu > 0:
        # Si c'est 0, c'est qu'il n'y a pas eu de population précédemment.
        # Et donc pas d'ancien meilleur.

        scoreMaxAncPop = lesAnciensMeilleurs_X8.meilleur_individu.score  # On récupère le score du meilleur individu
        ancienPlusFort = lesAnciensMeilleurs_X8.meilleur_individu





    print(scoreMaxAncPop, scoreMaxPop)
    if scoreMaxAncPop > scoreMaxPop:
        # S'il s'avère qu'on a pas su faire mieux par rapport à la dernière génération.

        for espece in lesEspeces:
            for id_individu in range(len(espece.lesIndividus)):
                # On remplace tout le monde par l'ancien meilleur individu.
                # Comme ça, on est sûr que le meilleur domine totalement.

                espece.lesIndividus[id_individu].copier(ancienPlusFort)
                assert espece.lesIndividus[id_individu].score == ancienPlusFort.score

    else:
        # Donc l'individu PlusFort est le meilleur individu jusqu'à présent.
        # Alors on le stocke lui et son espèce comme étant le meilleur.
        # Le précédent meilleur reste en mémoire au cas où, temporairement.
        lesAnciensMeilleurs_X8.nouveau_meilleur(lesEspeces[PlusFort.idEspece], PlusFort)
        lesAnciensMeilleurs_X8.inieme_individu += 1
    """

    # Maintenant, on va calculer le score pour chaque espèce.

    nbIndividuTotal = 0
    scoreMoyenneGlobal = 0  # Score moyen de TOUS les individus.
    leMeilleur = creer_individu()  # On va essayer de trouver le meilleur réseau.

    for espece in lesEspeces:
        espece.scoreMoyen = 0  # Score moyen de tous les individus l'espèce
        espece.scoreMax = 0  # Score maximum d'un individu de l'espèce

        for individu in espece.lesIndividus:
            espece.scoreMoyen += individu.score  # On calcul plus tard la moyenne
            scoreMoyenneGlobal += individu.score  # On calcul plus tard la moyenne
            nbIndividuTotal += 1

            if espece.scoreMax < individu.score:
                # On a trouvé un meilleur individu dans l'espèce
                espece.scoreMax = individu.score

                if leMeilleur.score < individu.score:
                    # Et si en plus, il est le meilleur individu trouvé depuis notre recherche.
                    # Alors on dit que c'est le meilleur
                    leMeilleur = individu

        #espece.scoreMoyen, espece.scoreMax)

        #  On calcule la moyenne de l'espèce :
        espece.scoreMoyen = espece.scoreMoyen / len(espece.lesIndividus)

    scoreMoyenneGlobal = scoreMoyenneGlobal / nbIndividuTotal

    trierEspecesParScoreMoyen(lesEspeces)

    #  Plus une espèce à un bon score, plus il pourra créer d'enfants.

    tabLEO = []

    for id_espece in range(len(lesEspeces)):
        espece = lesEspeces[id_espece]

        # Nombre d'enfants qu'aimerait faire l'espèce

        nbIndividuEspece = math.ceil(len(espece.lesIndividus) * espece.scoreMoyen / scoreMoyenneGlobal)

        # On supprime du nombre d'individus à créer le nombre d'individus que va créer l'espèce.
        nbIndividuACreer -= nbIndividuEspece

        # Si on s'aperçoit que l'espèce va créer plus d'individu qu'on peut se permettre.
        if nbIndividuACreer < 0:
            nbIndividuEspece += nbIndividuACreer  # On retire le surplus
            nbIndividuACreer = 0  # On remet à 0.

            # Remarque :
            # Il est possible qu'il ne reste plus de place pour des espèces.
            # Dans le cas, le surplus ce sont le nombre d'individus que va créer l'espèce.
            # Donc l'espèce ne pourra pas faire de bébé.

        espece.nbEnfants = nbIndividuEspece

        # print("enfant", espece.nbEnfants)
        # for ind in espece.lesIndividus:
        #    print("fkjdsfjhfdshjfdshjfdjssdfjh", ind.lesConnexions)

        for enfant in range(nbIndividuEspece):
            if len(espece.lesIndividus) >= 2:
                # On fait un crossover avec deux individus.
                # Si l'individu n'en a pas au moins 2, on ne le fait pas.

                unIndividu = crossover(choisirParent(espece.lesIndividus), choisirParent(espece.lesIndividus))
                # print(unIndividu)

                # print("hello")
                mutation(unIndividu)
                # print("connexions:",id(unIndividu),(unIndividu.lesConnexions))

                unIndividu.idEspece = id_espece
                unIndividu.score = 1
                tabLEO.append(unIndividu)
                laNouvellePopulation.append(unIndividu)
                indiceNouvelleEspece += 1
            else:
                # print("aaa")
                unIndividu = creer_individu()
                unIndividu.copier(espece.lesIndividus[0])
                mutation(unIndividu)

                # print("hello mono parent")
                tabLEO.append(unIndividu)
                laNouvellePopulation.append(unIndividu)
                # print("connexions:", id(unIndividu), (unIndividu.lesConnexions))

            ##print(laNouvellePopulation[enfant])

            ##for co in unIndividu.lesConnexions:
            ##print("1---",co)

            ##for co in laNouvellePopulation[enfant].lesConnexions:
            ##print("2---",co)

    # Si une espèce n'a pas fait d'enfant, on la supprime (car l'espèce a disparu)
    id_espece = 0
    while id_espece < len(lesEspeces):
        if lesEspeces[id_espece].nbEnfants == 0:
            del lesEspeces[id_espece]
        id_espece += 1

    ##print("say hello")

    ##for ind in laNouvellePopulation:
    ##    print(ind.lesConnexions)

    ##for ind in tabLEO:
    ##   print(ind.lesConnexions)

    return laNouvellePopulation


def horodatage():
    """
    Principe :
        Calcul l'horodatage actuel
    Sortie:
        date_formater       [STR] : Horodatage
    """
    date = datetime.now()
    m = '0' + str(date.month) if date.month < 10 else str(date.month)
    j = '0' + str(date.day) if date.day < 10 else str(date.day)
    h = '0' + str(date.hour) if date.hour < 10 else str(date.hour)
    mi = '0' + str(date.minute) if date.minute < 10 else str(date.minute)
    s = '0' + str(date.second) if date.second < 10 else str(date.second)

    date_formater = str(date.year) + m + j + '_' + h + mi + s + str(date.microsecond)
    return date_formater


def SAVE_ANCIENNES_POPULATIONS(l_ancienne_population, chemin=CHEMIN_SAVE_ANCIENNES_POPULATIONS):
    if type(l_ancienne_population) != list:
        print("ERREUR : IMPOSSIBLE DE SAUVEGARDER")
        return

    nom_f = 'ANCIENNES_POPULATIONS_DU_' + horodatage() + '.pop'
    f = open(chemin + nom_f, 'wb')  # Ouvre le fichier en écriture
    pickler = pickle.Pickler(f, pickle.HIGHEST_PROTOCOL)  # Je ne sais pas...
    pickler.dump(l_ancienne_population)  # Sauvegarde la liste population dans le fichier f.
    f.close()

    print("SAUVEGARDE >> Le fichier " + nom_f + " a bien été sauvegardé !")


inieme_ind_plus_fort_derniere_save = 0


def SAVE_INDIVIDU_PLUS_FORT(individu_plus_fort, lesAnciensMeilleurs_X8, chemin=CHEMIN_SAVE_INDIVIDU_PLUS_FORT):
    global inieme_ind_plus_fort_derniere_save
    # global itteration_bcl
    if type(individu_plus_fort) != INDIVIDU:
        print("ERREUR : IMPOSSIBLE DE SAUVEGARDER")
        return

    if inieme_ind_plus_fort_derniere_save < lesAnciensMeilleurs_X8.inieme_individu or True:
        inieme_ind_plus_fort_derniere_save = lesAnciensMeilleurs_X8.inieme_individu

        nom_f = str(itteration_bcl)+'INDIVIDU_PLUS_FORT' + horodatage() + '.ind'
        f = open(chemin + nom_f, 'wb')  # Ouvre le fichier en écriture
        pickler = pickle.Pickler(f, pickle.HIGHEST_PROTOCOL)  # Je ne sais pas...
        pickler.dump(individu_plus_fort)  # Sauvegarde la liste population dans le fichier f.
        f.close()

        print("SAUVEGARDE >> Le fichier " + nom_f + " a bien été sauvegardé !")

def recup_individu(nom_fichier, chemin):
    f = open(chemin + nom_fichier, "rb")
    individu_charger = pickle.load(f)
    f.close()

    return individu_charger

def SAVE_HISTORIQUE_POPULATIONS(population, chemin=CHEMIN_SAVE_HISTORIQUE_POPULATIONS):
    """
    Principe :
        Sauvegarde la population dans un fichier binaire.

        Remarque :  en principe on sauvegarde une population qui va être remplacé.
    Entrée :
        population      [LIST] : Liste d'individu représentant la population

    """
    if type(population) != list:
        print("ERREUR : IMPOSSIBLE DE SAUVEGARDER")
        return
    nom_f = 'POPULATION_DU_' + horodatage() + '.pop'
    f = open(chemin + nom_f, 'wb')  # Ouvre le fichier en écriture
    pickler = pickle.Pickler(f, pickle.HIGHEST_PROTOCOL)  # Je ne sais pas...
    pickler.dump(population)  # Sauvegarde la liste population dans le fichier f.
    f.close()

    print("SAUVEGARDE >> Le fichier " + nom_f + " a bien été sauvegardé !")


def SAVE_RAPPORT(rapport, chemin=CHEMIN_SAVE_RAPPORT):
    # voir https://python.doctor/page-lire-ecrire-creer-fichier-python
    # nom_f = "RAPPORT.txt"
    # global itteration_bcl
    nom_f = str(itteration_bcl)+"RAPPORT" + horodatage() + '.txt'

    if type(rapport) == str:

        fichier = open(chemin + nom_f, "w")  # Note: mettre a pour Ouvre en écriture à la suite le fichier
        fichier.write("\n" + rapport)  # Écrit dans le fichier, à la suite
        fichier.close()  # Ferme le fichier

        print("SAUVEGARDE >> Le fichier " + nom_f + " a bien été sauvegardé !")
    elif type(rapport) == list:
        fichier = open(chemin + nom_f, "w")
        for ligne in rapport:
            if type(ligne) == str:
                fichier.write("\n" + ligne)
        fichier.close()

        print("SAUVEGARDE >> Le fichier " + nom_f + " a bien été sauvegardé !")
    else:
        print("ERREUR : IMPOSSIBLE DE SAUVEGARDER")


def test_save_meilleur_pop(pop):
    nom_f = "meilleur_pop" + horodatage() + '.pop'

    print("SAUVEGARDE >> Save meilleur pop OneDrive")

    f = open(CHEMIN_SAVE_ONEDRIVE + nom_f, 'wb')  # Ouvre le fichier en écriture
    pickler = pickle.Pickler(f, pickle.HIGHEST_PROTOCOL)  # Je ne sais pas...
    pickler.dump(pop)  # Sauvegarde la liste population dans le fichier f.
    f.close()


def SAVE_ONEDRIVE(individu_plus_fort, rapport, console_en_direct, lesAnciensMeilleurs_X8):
    # Sauvegarde sur OneDrive
    # individu_plus_fort → INDIVIDU
    # rapport → texte ou liste
    # console_en_direct → liste     ["CONSOLE", "ligne 2", "ligne 3...."]

    global DERNIER_SAUVEGARDE_ONEDRIVE

    """
    if DERNIER_SAUVEGARDE_ONEDRIVE is not None:  # Si on a déjà fait une sauvegarde sur OneDrive
        if int(DERNIER_SAUVEGARDE_ONEDRIVE[11:13]) + 2 > int(
                horodatage()[11:13]):  # Si on est encore sur la même minute
            # Alors on ne sauvegarde pas
            return
    """
    # Soit DERNIER_SAUVEGARDE_ONEDRIVE est None,
    # Soit on est passé à une autre minute depuis la dernière sauvegarde

    DERNIER_SAUVEGARDE_ONEDRIVE = horodatage()

    print("SAUVEGARDE >> Enregistrement sur OneDrive...")

    SAVE_INDIVIDU_PLUS_FORT(individu_plus_fort, lesAnciensMeilleurs_X8, CHEMIN_SAVE_ONEDRIVE)
    # SAVE_RAPPORT(rapport, CHEMIN_SAVE_ONEDRIVE)

    if type(console_en_direct) == list:
        # fichier = open(CHEMIN_SAVE_ONEDRIVE + "CONSOLE_EN_DIRECT.txt", "w")  # ATTENTION: Écrase le fichier !
        fichier = open(CHEMIN_SAVE_ONEDRIVE + "CONSOLE_EN_DIRECT" + horodatage() + '.txt',
                       "w")  # ATTENTION: Écrase le fichier !

        horo = horodatage()
        horodatage_au_propre = horo[6:8] + "/" + horo[4:6] + "/" + horo[:4] + " A " + horo[9:11] + ":" + horo[11:13]
        fichier.write("== AFFICHAGE CONSOLE EN DIRECT DU " + horodatage_au_propre + " ==\n")

        for ligne in console_en_direct:
            if type(ligne) == str:
                fichier.write("\n" + ligne)
        fichier.close()
        print("SAUVEGARDE >> Le fichier CONSOLE_EN_DIRECT.txt a bien été sauvegardé !")
    else:
        print("ERREUR : Impossible de sauvegarder la console en direct ,ce n'es pas une liste")

    print("SAUVEGARDE >> Les fichiers ont été envoyés vers OneDrive (normalement)")





def maj_msg_console(objet_info, LESANCIENSMEILLEURS_X8, nb_generation, tps_boucle, len_les_especes,
                    MEILLEUR_SCORE_FIN_PARTIE, premiere_partie):
    objet_info.no_generation = nb_generation
    objet_info.nb_espece = len_les_especes
    objet_info.temps_boucle = tps_boucle

    if not premiere_partie:
        objet_info.meilleur_score = LESANCIENSMEILLEURS_X8.meilleur_individu.score
        objet_info.score_moyen_espece = LESANCIENSMEILLEURS_X8.meilleur_espece.scoreMoyen
        objet_info.len_liste_connexions = len(LESANCIENSMEILLEURS_X8.meilleur_individu.lesConnexions)
        objet_info.len_liste_neurones = len(LESANCIENSMEILLEURS_X8.meilleur_individu.lesNeurones)
        objet_info.id_espece_du_meilleur = LESANCIENSMEILLEURS_X8.meilleur_individu.idEspece
        objet_info.meilleur_score_fin_partie = MEILLEUR_SCORE_FIN_PARTIE
    else:
        objet_info.meilleur_score = "PAS ENCORE PRIS EN COMPTE"
        objet_info.score_moyen_espece = "PAS ENCORE PRIS EN COMPTE"
        objet_info.len_liste_connexions = "PAS ENCORE PRIS EN COMPTE"
        objet_info.len_liste_neurones = "PAS ENCORE PRIS EN COMPTE"
        objet_info.id_espece_du_meilleur = "PAS ENCORE PRIS EN COMPTE"
        objet_info.meilleur_score_fin_partie = "PAS ENCORE PRIS EN COMPTE"


def affiche_info_IA(obj):
    for ligne in obj.retourne_liste_info(obj):
        print("\n" + str(ligne))





def generateur(monIA, importe_population):
    #global maxscore
    #global MEILLEUR_SCORE_FIN_PARTIE
    MEILLEUR_SCORE_FIN_PARTIE = 0
    MEILLEUR_RAPPORT = []
    lesAnciensMeilleurs_X8 = LESANCIENSMEILLEURS()

    print(">>> Lancement du générateur")
    temps_debut = time.time()

    # La Pré Population ⇒ Préparatif avant de créer une vraie population
    laPrePopulation = creer_population()  # On crée une population d'individu


    if importe_population != []:
        laPrePopulation = []
        for ind_creer in range(4):
            if ind_creer < len(importe_population):
                ind = creer_individu()
                ind.copier(importe_population[ind_creer])

                laPrePopulation.append(ind)

            else:
                ind = creer_individu()
                laPrePopulation.append(ind)


    """
    mutation(laPrePopulation[0])

    for i in range(1, len(laPrePopulation)):  # Afin d'avoir des copies évoluées du premier individu
        laPrePopulation[i].copier(laPrePopulation[0])
        mutation(laPrePopulation[i])
    """

    lesEspeces = trierPopulation(laPrePopulation)


    # la vraie population qu'on va utiliser
    laPopulation = nouvelleGeneration(laPrePopulation, lesEspeces, lesAnciensMeilleurs_X8)

    # for generation in range(5000000):

    generation = -1
    while generation < 30000:
        id_meilleur_pr_rapport = lesAnciensMeilleurs_X8.inieme_individu



        generation += 1

        liste_joueurs = [monIA for i in range(len(laPopulation))]

        # LANCEMENT D'UNE PARTIE

        # 5 manches     | Liste de joueurs (notre IA) | Les différents réseaux de neurone propre à chaque IA.
        resultat_partie = partie_diamant(5, liste_joueurs, laPopulation)

        # On récupère le nombre de diamants de tous les joueurs à la fin de la partie.
        nbdiamants_tous_les_joueurs = resultat_partie[0]

        # On récupère la liste des joueurs après la fin de la partie (ATTENTION : cela ne correspond pas à la classe Joueur_X8)
        lesJoueursPartie = resultat_partie[1]

        # On récupère laPopulation (la liste des individus qu'on avait distribués aux différents joueurs IA Picsou)
        laPopulation = resultat_partie[2]

        rapp = resultat_partie[3]

        nbdiamants_tous_les_joueurs_malus = nbdiamants_tous_les_joueurs.copy()

        if nbdiamants_tous_les_joueurs_malus:
            for id_joueur in range(len(nbdiamants_tous_les_joueurs_malus)):
                joueur = lesJoueursPartie[id_joueur].Picsou_objet_joueur_X8

                if joueur.etat_historique.count('M') > 0:
                    nbdiamants_tous_les_joueurs_malus[id_joueur] -= 20 * joueur.etat_historique.count(
                        'M')  # On lui retire des diamants, car il a osé mourir

        """
        msfp_avant = MEILLEUR_SCORE_FIN_PARTIE
        MEILLEUR_SCORE_FIN_PARTIE = (max(max(nbdiamants_tous_les_joueurs), MEILLEUR_SCORE_FIN_PARTIE))
        """

        #msfp_avant = MEILLEUR_SCORE_FIN_PARTIE
        MEILLEUR_SCORE_FIN_PARTIE = (max(max(nbdiamants_tous_les_joueurs_malus), MEILLEUR_SCORE_FIN_PARTIE))

        """
        for individu in laPopulation:
            if individu.score > maxscore:
                maxscore = individu.score
        """

        # print("sdfhsdjd", les
        # print("score max", maxscore, generation, time.strftime("%H:%M:%S", time.gmtime(int(time.time() - temps_debut))))
        #print(nbdiamants_tous_les_joueurs)

        """
        for i in lesJoueursPartie:
            print("stats resultat partie :", nbdiamants_tous_les_joueurs)
            print("Historique etat :", i.Picsou_objet_joueur_X8.etat_historique)
            print("Historique nb tour resté :", i.Picsou_objet_joueur_X8.nb_tour_rester_ds_manche_historique)
        """

        """
        for i in(nbdiamants_tous_les_joueurs):
            print("====", id(i))
        """

        if generation == 0:
            premiere_partie = True
        else:
            premiere_partie = False

        maj_msg_console(objet_info, lesAnciensMeilleurs_X8, generation,
                        time.strftime("%H:%M:%S", time.gmtime(int(time.time() - temps_debut))), len(lesEspeces),
                        MEILLEUR_SCORE_FIN_PARTIE, premiere_partie)

        affiche_info_IA(objet_info)
        # SAVE_ONEDRIVE(lesAnciensMeilleurs_X8.meilleur_individu, "", objet_info.retourne_liste_info(objet_info))

        """
        if msfp_avant < MEILLEUR_SCORE_FIN_PARTIE:
            test_save_meilleur_pop(laPopulation)
        """


        # SAVE_INDIVIDU_PLUS_FORT(lesAnciensMeilleurs_X8.meilleur_individu)

        ##print("patateee")
        ##for ind in laPopulation:
        ##    print("      --- ",ind.lesConnexions)

        lesEspeces = trierPopulation(laPopulation)
        laPopulation = nouvelleGeneration(laPopulation, lesEspeces, lesAnciensMeilleurs_X8, nbdiamants_tous_les_joueurs, lesJoueursPartie)

        if id_meilleur_pr_rapport != lesAnciensMeilleurs_X8.inieme_individu:
            MEILLEUR_RAPPORT = rapp

        """
        if msfp_avant < MEILLEUR_SCORE_FIN_PARTIE:
            SAVE_ONEDRIVE(lesAnciensMeilleurs_X8.meilleur_individu, "", objet_info.retourne_liste_info(objet_info))
            SAVE_RAPPORT(rapp, CHEMIN_SAVE_ONEDRIVE)
        """

    # Combien de temps le programme a fonctionné.
    #temps_fin = time.time()
    """
    print(">>> Durée de fonctionnement du programme:",
          time.strftime("%H:%M:%S", time.gmtime(int(temps_fin - temps_debut))))
    """
    return lesAnciensMeilleurs_X8.meilleur_individu, MEILLEUR_RAPPORT, lesAnciensMeilleurs_X8
"""
def boucle_generateur():
    laPopulationImport = []
    for tour_generateur in range(25):
        print("itteration_bcl:", itteration_bcl, "tour générateur:",tour_generateur)
        res = generateur('IA_PipoX8_EPREPA', laPopulationImport)
        individu_gagnant = res[0]
        rapport = res[1]
        lesAnciensMeilleurs_X8 = res[2]



        #if rapport != []:
        SAVE_INDIVIDU_PLUS_FORT(individu_gagnant, lesAnciensMeilleurs_X8, "save_pickle/test/")
        SAVE_RAPPORT(rapport, "save_pickle/test/")




        meilleur_individu = individu_gagnant
        #meilleur_individu.copier(individu_gagnant)

        assert meilleur_individu.score == individu_gagnant.score
        assert meilleur_individu.nbNeurones == individu_gagnant.nbNeurones

        # save_meilleur_tour_generateur(meilleur_individu,"save_pickle/")
        # SAVE_INDIVIDU_PLUS_FORT(meilleur_individu, CHEMIN_SAVE_INDIVIDU_PLUS_FORT_TOUR_GENERATEUR)

        if len(laPopulationImport) <= 4:
            laPopulationImport.append(meilleur_individu)
        else:
            laPopulationImport = []
            laPopulationImport.append(meilleur_individu)

        #print("tour generateur suivant:", tour_generateur + 1)
        # time.sleep(0.5)
"""
def boucle_generateur():
    laPopulationImport = [recup_individu("0INDIVIDU_PLUS_FORT20230114_195632765409.ind","MEILLEUR_INDIVIDU/test/bien/")]
    laPopulationImport = []
    for tour_generateur in range(30):
        print("itteration_bcl:", itteration_bcl, "tour générateur:",tour_generateur)
        res = generateur('IA_Picsou', laPopulationImport)
        individu_gagnant = res[0]
        rapport = res[1]
        lesAnciensMeilleurs_X8 = res[2]



        #if rapport != []:
        SAVE_INDIVIDU_PLUS_FORT(individu_gagnant, lesAnciensMeilleurs_X8, "save_pickle/test/")
        SAVE_RAPPORT(rapport, "save_pickle/test/")




        meilleur_individu = individu_gagnant
        #meilleur_individu.copier(individu_gagnant)

        assert meilleur_individu.score == individu_gagnant.score
        assert meilleur_individu.nbNeurones == individu_gagnant.nbNeurones

        # save_meilleur_tour_generateur(meilleur_individu,"save_pickle/")
        # SAVE_INDIVIDU_PLUS_FORT(meilleur_individu, CHEMIN_SAVE_INDIVIDU_PLUS_FORT_TOUR_GENERATEUR)

        laPopulationImport = []

        4


        """
        if len(laPopulationImport) <= 3:
            laPopulationImport.append(meilleur_individu)
        else:
            laPopulationImport = []
            laPopulationImport.append(meilleur_individu)
        """

        #print("tour generateur suivant:", tour_generateur + 1)
        # time.sleep(0.5)




for i in range(1):
    itteration_bcl = i
    boucle_generateur()

#boucle_generateur()

#generateur('IA_PipoX8_EPREPA', [])




"""
pop = creer_population()
mutation(pop)
"""
"""
pop = creer_population()
while True:
    SAVE_ONEDRIVE(pop[0], "patate", ["sous"])
"""

"""
pop = creer_population()

print(pop[0].lesNeurones[0].typeNeurone)
ajouter_neurone(pop[0], 2, "CACHER", 5)
ajouter_connexion(pop[0], 0, 3)


SAVE_HISTORIQUE_POPULATIONS(pop)
SAVE_INDIVIDU_PLUS_FORT(pop[0])
"""
