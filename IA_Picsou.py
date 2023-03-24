##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

# IA de Matthieu et Tom - IUT de Vélizy
# Toute réutilisation de notre travail sans notre accord est interdite


from random import *

NB_INPUT = 7  # Nombre de neurones d'entrée
NB_OUTPUT = 2  # Nombre de neurones de sortie

#===========================================================================================
class NEURONE:
    # Créer un neurone vide
    # Note : Inspiré du travail du vidéaste Laupok.

    def __init__(self, valeur, id, typeNeurone):
        self.valeur = valeur  # Valeur du neurone par défaut
        self.id = id  # Id par défaut d'un neurone créer (devra être changé).
        self.typeNeurone = typeNeurone # Type de neurone (INPUT, OUTPUT, CACHER)

    def copier(self, neurone_a_copier):
        self.valeur = neurone_a_copier.valeur
        self.id = neurone_a_copier.id
        self.typeNeurone = neurone_a_copier.typeNeurone

class CONNEXION:
    def __init__(self, innovation, entree, sortie, actif, poids):
        self.innovation = innovation  # Identifiant unique de la connexion. Indique que c'est l'innovation ème connexion.
        self.entree = entree  # Neurone d'entrée
        self.sortie = sortie  # Neurone de sortie
        self.actif = actif  # Le neurone est actif ou mort
        self.poids = poids  # Poids de la connexion

    def copier(self, connexion_a_copier):
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
            connexion_cree.copier(connexion_a_copier)

            self.lesConnexions.append(connexion_cree)


        self.nbInnovationConnexions = individu_a_copier.nbInnovationConnexions

def creer_neurone(): return NEURONE()

def creer_connexion(): return CONNEXION()

#=========================================================================================

class IA_Diamant:
    def __init__(self, match: str):
        """Génère l'objet de la classe IA_Diamant

        Args:
            match (str) : descriptif de la partie

            # Pour les tests :
                dico_de_decisions = Dictionnaire Au format TITRE_INFO : INFO
                Sera prise en compte et modifiée pour prendre les meilleures décisions durant une manche
        """

        self.no_manche = 0
        # Deck de jeu du début de la manche (mis à jour à la fin d'une manche, pour la suivante)
        self.init_deck_tresors = [1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17]
        self.init_deck_pieges = {"P1": 3, "P2": 3, "P3": 3, "P4": 3, "P5": 3}
        self.init_deck_valeurs_reliques = [5, 5, 5, 10, 10]

        # Deck de jeu au cours de la manche (mis à jour à chaque tour)
        self.manche_deck_tresors = [1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17]
        self.manche_deck_pieges = {"P1": 3, "P2": 3, "P3": 3, "P4": 3, "P5": 3}

        match_traduit = decoupage_str(match)

        self.nb_manche_partie = match_traduit[0]  # pour récupérer le nb de manche pour la partie

        self.l_joueurs = creer_joueur(match_traduit[1], match_traduit[2], match_traduit[3], self)


        self.Picsou_objet_joueur_X8 = None
        for joueur in self.l_joueurs:
            if joueur.cest_moi:
                self.Picsou_objet_joueur_X8 = joueur
        assert type(self.Picsou_objet_joueur_X8) == Joueur_X8, "Erreur: L'objet joueur de Picsou n'a pas été trouvé ?"


        # Liste lier à la manche actuelle
        self.no_tour = 0
        self.liste_dangers_banc = []
        self.nb_reliques_banc = 0

        self.liste_dangers_elimine_jeu = []

        self.reste_tresor = 0

        self.nb_joueur_sorti = 0
        self.nb_joueur_explore = 0

        self.nb_relique_en_jeu_nn_sortie = 0
        self.nb_carte = len(self.init_deck_tresors) + sum(
            self.init_deck_pieges.values()) + self.nb_relique_en_jeu_nn_sortie  # calcule le nb de carte du deck au début d'une manche
        # et est mise à jour au fur et à mesure des tours

        self.individuDePicsou = INDIVIDU()

        devine_valeur("", self, True)  # On indique à l'IA que c'est une nouvelle manche
        self.init_individu()

    def init_individu(self):

        # Création des neurones
        self.individuDePicsou.lesNeurones.append(NEURONE(7, 0, "INPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(4, 1, "INPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(1, 2, "INPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(7, 3, "INPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(9.571428571428571, 4, "INPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(0.14285714285714285, 5, "INPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(-0.2857142857142857, 6, "INPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(10.5, 7, "OUTPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(8.375, 8, "OUTPUT"))
        self.individuDePicsou.lesNeurones.append(NEURONE(21.0, 9, "CACHER"))
        self.individuDePicsou.lesNeurones.append(NEURONE(-10.5, 10, "CACHER"))

        # Création des connexions

        self.individuDePicsou.lesConnexions.append(CONNEXION(128810, 9, 7, True, 3.5))
        self.individuDePicsou.lesConnexions.append(CONNEXION(132831, 0, 7, True, 1.5))
        self.individuDePicsou.lesConnexions.append(CONNEXION(132832, 0, 10, True, -1.5))
        self.individuDePicsou.lesConnexions.append(CONNEXION(132833, 10, 9, True, -2.0))






    def action(self, tour: str) -> str:
        """Appelé à chaque décision du joueur IA

        Args :
            tour (str): descriptif du dernier tour de jeu

        Returns :
            str : 'X' ou 'R'
        """

        # ================================= PLAN A
        # A quoi consiste le plan A ?
        # Picsou analyse de manière totalement autonome la situation et prend sa décision de lui-même.

        majReseau(self.individuDePicsou, self.Picsou_objet_joueur_X8, self, tour)  # On met à jour les neurones d'entrées
        feedForward(self.individuDePicsou)  # On met à jour le réseau de neurone (en dehors des INPUTS).
        decision_plan_A = priseDeDecision(
            self.individuDePicsou)  # On prend la décision : 'R' pour partir, 'X' sinon.

        # ================================= PLAN B
        # A quoi consiste le plan B ?
        # À vérifier que notre décision était bonne, et à la réajuster s'il le faut


        #decision_plan_B = self.verif_par_plan_b(decision_plan_A)



        # ================================= PLAN C
        # A quoi consiste le plan C ?
        # Au bout d'un moment, Picsou peut s'apercevoir qu'il est en difficulté.
        # En effet, ce n'est pas le meilleur joueur.
        # Dans ce cas-là, Picsou devra analyser ses adversaires.
        # En fonction d'eux, il va voir pour rester plus, ou moins longtemps dans une manche.
        # Cela forme un nouveau nombre qu'on multipliera avec priseDeDecision(self.individuDePicsou).

        decision_final = decision_plan_A


        """
        alea = randint(0, 1)

        if alea == 0:
            return 'X'
        else:
            'R'
        """

        return decision_final

    def fin_de_manche(self, raison: str, dernier_tour: str) -> None:
        """Appelé à chaque fin de manche

        Args :
            raison (str) : 'R' si tout le monde est un piège ou "P1","P2", ... si un piège a été déclenché
            dernier_tour (str) : descriptif du dernier tour de la manche
        """

        devine_valeur(dernier_tour, self, False)  # On prend en compte le dernier tour
        devine_valeur(dernier_tour, self, True)  # On prépare à la nouvelle manche

        pass

    def game_over(self, scores: str) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args :
            scores (str): descriptif des scores de fin de jeu
        """

        # On met à jour le score de l'individu
        # Note : On initialise l'individu avec un score de + 1 dans notre fonction qui génère les générations.
        #        Donc on garde ce point d'avance par + 1.
        #        Comme ça, tous les individus sont égaux, même celui qui partirait dès les premiers tours.
        self.individuDePicsou.score = self.Picsou_objet_joueur_X8.inv_partie + 1


    # ============Méthode=============
    def remise_zero_nv_manche(self):
        self.manche_deck_tresors = [1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17]
        self.manche_deck_pieges = self.init_deck_pieges
        self.no_tour = 0
        self.liste_dangers_banc = []
        self.nb_reliques_banc = 0
        self.reste_tresor = 0

        self.nb_carte = len(self.init_deck_tresors) + sum(
            self.init_deck_pieges.values()) + self.nb_relique_en_jeu_nn_sortie  # calcule le nb de carte du deck au début d'une manche
        # et est mise à jour au fur et à mesure des tours

    def verif_par_plan_b(self, decision_plan_A):
        resultatSortir, resultatRester = decision_plan_A[0], decision_plan_A[1]

        #print("resultatSortir:", resultatSortir)
        #print("resultatRester:", resultatRester)

        #print(resultatSortir, resultatSortir > resultatRester)

        if compte_danger(self) > 2:
            resultatSortir = resultatSortir / 500

        #print(resultatSortir, resultatSortir > resultatRester)

        if self.reste_tresor > 3:
            resultatSortir = resultatSortir / 500

        if self.nb_joueur_sorti < 1:
            resultatSortir = resultatSortir * 50

        #if ratio_tresor_reste_possible(self) > 8:
        #    resultatRester = resultatRester + 500

        #print(resultatSortir, resultatSortir > resultatRester)
        #time.sleep(5)

        if resultatSortir > resultatRester:
            #print(">>> Decision: Partir")
            #time.sleep(5)
            return 'R'
        else:
            #print(">>> Decision: Rester")
            #time.sleep(5)
            return 'X'

#===============================================================================================

class Joueur_X8:
    def __init__(self, no_joueur, pseudonyme, cest_moi):
        self.no_joueur = no_joueur  # N° associé au joueur
        self.pseudonyme = pseudonyme  # Pseudo du joueur
        self.cest_moi = cest_moi    # Si True → cet objet est l'IA.
                                    # Si False → C'est un rival


        self.inv_manche = 0  # Le nombre de diamants récupérer durant la manche
        self.inv_partie = 0  # Le nombre de diamants protéger dans son repaire
        self.etat = "X"  # L'état du joueur dans la partie : [En_jeu/Partie]
        self.inv_relique = 0  # Le nombre de reliques récupérées par le joueur


        self.nb_tour_rester_ds_manche_historique = []  # Historique du nombre de tours resté par manche
        self.inv_historique = []  # Historique sous forme de liste du total des diamants récupéré par manche.
        self.etat_historique = []  # Historique sous forme de liste retraçant si le joueur a quitté de lui la manche ou non

        self.nb_danger_banc_historique = []  # Historique du nombre de dangers sur le banc lorsque le joueur est parti
        self.nb_reste_tresor_historique = []  # Historique du nombre restant de diamant dans le reste trésor lorsque le joueur est parti



    def init_historique(self,IA_Diamant): # A executer au début de la partie
        self.nb_tour_rester_ds_manche_historique = [0] * IA_Diamant.nb_manche_partie
        self.inv_historique = [0] * IA_Diamant.nb_manche_partie
        self.etat_historique = [0] * IA_Diamant.nb_manche_partie
        self.nb_danger_banc_historique = [0] * IA_Diamant.nb_manche_partie
        self.nb_reste_tresor_historique = [0] * IA_Diamant.nb_manche_partie

    def remise_zero_joueur_nv_manche(self):
        self.inv_manche = 0
        self.etat = "X"  #peut être pas obligatoire




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
#===============================================================================================

def conversion_str_int(a_convertir : str):
    """
    Principe :
        Si la variable en paramètre est un str qui cache un entier, alors on le converti en int.
        Sinon, on le renvoie tel quel
    Entrée :
        a_convertir         [STR] : A convertir (ou pas)
    Sortie :
        converti            [INT] : STR converti en INT
        *OU*
        a_convertir         [STR] : Dans le cas où on ne peut pas convertir
    """

    if type(a_convertir) != str:
        return a_convertir

    elif a_convertir.isdigit():  # On peut convertir
        converti = int(a_convertir)
        return converti
    else:
        return a_convertir

def decoupage_str(str_a_decouper : str):
    """
    Principe :
        Découpe le STR reçus par les différentes méthodes de la classe IA_Diamant en variables dans une liste.

        Il ajoute à variable un à un chaque caractère jusqu'à rencontrer |.
        Il ajoute alors variable dans format_utilisable et vide variable.
        S'il rencontre "," dans ce cas, il ajoute variable dans sous_liste et reset variable.

        A noté, que la fonction sait quand se termine sous_liste et format_utilisable.
    Entrée :
        str_a_decouper          [STR] : Suite de caractère à découper.
                                        Attention : les valeurs doivent être séparées par "|" et "," si dans une liste.
    Sortie :
        format_utilisable      [LIST] : Liste regroupant les valeurs ou listes que contenait str_a_decouper
    """
    assert type(str_a_decouper) == str, "ERREUR Ce n'est pas un str"

    format_utilisable = []              # Liste contenant le contenu du str, mais dans un meilleur format
    variable = ""                       # variable qui sera peut-être ajouté dans format_utilisable ou sous_liste
    sous_liste = []                     # liste qui sera peut-être ajoutée dans format_utilisable


    for caractere_id in range(len(str_a_decouper)):
        caractere = str_a_decouper[caractere_id]
        caractere_suivant = ""

        if caractere_id + 1 == len(str_a_decouper):  # Si on a atteint le dernier caractère de str_a_decouper, on clôture format_utilisable
            if not sous_liste:  # Si on n'utilise pas sous_liste
                format_utilisable.append(
                    conversion_str_int(variable + caractere)
                )
                return format_utilisable

            else:  # Si on s'en sert, on doit la clôturer et l'ajouté juste avant.
                sous_liste.append(
                    conversion_str_int(variable + caractere)
                )
                format_utilisable.append(sous_liste)
                return format_utilisable

        else:
            caractere_suivant = str_a_decouper[caractere_id + 1]  # sinon on stocke le caractère qui suit

        if caractere not in ['|', ',']:

            variable += caractere

            if caractere_suivant == '|':
                # On a atteint la fin de la variable, on passe à tout autre chose

                if not sous_liste:  # Si on n'utilise pas sous_liste
                    format_utilisable.append(
                        conversion_str_int(variable)
                    )
                else:
                    sous_liste.append(
                        conversion_str_int(variable)
                    )
                    format_utilisable.append(sous_liste)

                # On réinitialise pour accueillir la prochaine variable
                variable = ""
                sous_liste = []

            elif caractere_suivant == ',':
                # On a atteint la fin d'une variable dans la liste, on passe à la variable suivante de cette liste

                sous_liste.append(
                    conversion_str_int(variable)
                )

                # On réinitialise pour accueillir la prochaine variable
                variable = ""


        # print(caractere)
    return format_utilisable

#================================================================================================

# PARTIE : Récupère les infos reçues par le bot et essaye d'en déduire un maximum de valeur

def devine_valeur(tour, IA_diamant, preparatif_prochaine_manche):
    """
        Permet de récupérer et de stocker la plupart des informations concernant la partie,
        et les stock dans la class IA_diamant et Joueur_X8
        :param tour:                        [str]        : décrit la décision des joueurs et la carte tiré ce tour
        :param IA_diamant:                  [IA_diamant] : class représentant l'IA
        :param preparatif_prochaine_manche: [Bool]       : indique si c'est le premier tour d'une manche ou pas
        :return: None
        """
    # tour → str des infos du tour
    # IA_Diamant → Picsou
    # preparatif_prochaine_manche → BOOL True s'il faut se préparer à la nouvelle manche
    info_tour = decoupage_str(tour)


    if preparatif_prochaine_manche:  # si nouvelle manche reçoit True pour preparatif_prochaine_manche
        if IA_diamant.no_manche > 0:
            remise_zero_nv_manche(IA_diamant)

        IA_diamant.nb_carte += 1  # rajoute une relique
        IA_diamant.nb_relique_en_jeu_nn_sortie += 1

        IA_diamant.no_manche += 1
        IA_diamant.no_tour = 0

        return


    dec_joueur(info_tour, IA_diamant)

    liste_decision = info_tour[0]
    carte_tiree = info_tour[1]

    IA_diamant.nb_carte -= 1
    IA_diamant.no_tour += 1

    if liste_decision.count("R") >= 1:
        for i in range(len(liste_decision)):
            joueur = IA_diamant.l_joueurs[i]
            if liste_decision[i] == "R":

                joueur.inv_partie += joueur.inv_manche + (
                        IA_diamant.reste_tresor // IA_diamant.nb_joueur_sorti)  # inv manche pas n'est remis à zero


        IA_diamant.reste_tresor = IA_diamant.reste_tresor % max(IA_diamant.nb_joueur_sorti, 1)

    if carte_tiree in IA_diamant.manche_deck_tresors:  # carte sortie trésor
        IA_diamant.manche_deck_tresors.remove(carte_tiree)
        for i in range(len(liste_decision)):
            joueur = IA_diamant.l_joueurs[i]
            if liste_decision[i] == "X":
                joueur.inv_manche += carte_tiree // IA_diamant.nb_joueur_explore

        IA_diamant.reste_tresor += carte_tiree % max(IA_diamant.nb_joueur_explore,1)
    elif carte_tiree in ["P1", "P2", "P3", "P4", "P5"]:  # carte sortie danger

        if carte_tiree not in IA_diamant.liste_dangers_banc:
            IA_diamant.liste_dangers_banc.append(carte_tiree)
            IA_diamant.manche_deck_pieges[carte_tiree] -= 1
        else:
            # on supprime le piege
            IA_diamant.liste_dangers_elimine_jeu.append(carte_tiree)
            IA_diamant.init_deck_pieges[carte_tiree] -= 1
            for i in range(len(liste_decision)):
                if liste_decision[i] == "X":
                    joueur = IA_diamant.l_joueurs[i]
                    joueur.nb_tour_rester_ds_manche_historique[IA_diamant.no_manche - 1] = IA_diamant.no_tour
                    joueur.inv_historique[IA_diamant.no_manche - 1] = 0
                    joueur.etat_historique[IA_diamant.no_manche - 1] = "M"  # Mort
                    joueur.nb_danger_banc_historique[IA_diamant.no_manche - 1] = len(
                        IA_diamant.liste_dangers_banc)  # nb danger sur le banc sans le deuxieme exemplaire du danger qui fini la manche
                    joueur.nb_reste_tresor_historique[
                        IA_diamant.no_manche - 1] = IA_diamant.reste_tresor  # reste trésor avant que la manche ne se coupe



    elif carte_tiree == "R":  # carte sortie relique
        IA_diamant.nb_reliques_banc += 1
        IA_diamant.nb_relique_en_jeu_nn_sortie -= 1

        if IA_diamant.nb_joueur_sorti == 1:
            for i in range(len(liste_decision)):
                if liste_decision[i] == "R":
                    for relique in range(IA_diamant.nb_reliques_banc):
                        IA_diamant.l_joueurs[i].inv_partie += IA_diamant.init_deck_valeurs_reliques[0]
                        IA_diamant.l_joueurs[i].inv_relique += 1
                        IA_diamant.nb_reliques_banc -= 1
                        del IA_diamant.init_deck_valeurs_reliques[0]

    IA_diamant.nb_joueur_sorti = 0
    IA_diamant.nb_joueur_explore = 0

    # Maintenant, on doit considérer les joueurs qui viennent de partir de la grotte comme rentré chez eux.
    # Sinon, on va les considérés comme s'ils ils quittaient à chaque tour.
    if liste_decision.count("R") >= 1:
        for i in range(len(liste_decision)):
            joueur = IA_diamant.l_joueurs[i]
            if liste_decision[i] == "R":
                joueur.etat = 'N'

def dec_joueur(info_tour, IA_diamant):
    """
    Compte le nombre de joueur qui continue l'exploration et le nombre de joueur qui rentre
    et met à jour les variables d'historique dans les class Joueur_X8 de chaque joueur.
    :param info_tour:                   [list]
    :param IA_diamant:                  [IA_diamant] : class représentant l'IA
    :return: None
    """
    liste_decision = info_tour[0]

    for i in range(len(liste_decision)):
        joueur = IA_diamant.l_joueurs[i]
        if liste_decision[i] == "X":
            IA_diamant.nb_joueur_explore += 1
            joueur.etat = "X"
        elif liste_decision[i] == "R":
            IA_diamant.nb_joueur_sorti += 1

            joueur.etat = "R"  # Peut-être mettre direct "N" au lieu de "R"
            joueur.nb_tour_rester_ds_manche_historique[IA_diamant.no_manche - 1] = IA_diamant.no_tour
            joueur.inv_historique[IA_diamant.no_manche - 1] = joueur.inv_manche
            joueur.etat_historique[IA_diamant.no_manche - 1] = "V" # Vivant
            joueur.nb_danger_banc_historique[IA_diamant.no_manche - 1] = len(IA_diamant.liste_dangers_banc)
            joueur.nb_reste_tresor_historique[IA_diamant.no_manche - 1] = IA_diamant.reste_tresor  # reste trésor juste avant qu'il soit partie donc pas encore partager entre tous ceux sortis



def remise_zero_nv_manche(IA_diamant):
    """
    Appelle les méthodes de réinitialisation pour les class IA_Diamant et Joueur_X8
    :param IA_diamant:                  [IA_diamant] : class représentant l'IA
    :return: None
    """
    IA_diamant.remise_zero_nv_manche()
    for joueur in IA_diamant.l_joueurs:
        joueur.remise_zero_joueur_nv_manche()


def proba_appart_tresor(IA_diamant):
    """
    Calcule la probabilité qu'une carte trésor sorte au prochain tour
    :param : IA_diamant:                  [IA_diamant] : class représentant l'IA
    :return: proba_appart_tresor          [float]
    """
    return sum(IA_diamant.manche_deck_tresors) / max(IA_diamant.nb_carte,1)


def proba_appart_relique(IA_diamant):
    """
    Calcule la probabilité qu'une relique sorte au prochain tour
    :param : IA_diamant:                  [IA_diamant] : class représentant l'IA
    :return: proba_appart_relique         [float]
    """
    return IA_diamant.nb_relique_en_jeu_nn_sortie / max(IA_diamant.nb_carte,1)


def proba_appart_danger(IA_diamant):
    """
    Calcule la probabilité qu'une carte danger sorte au prochain tour
    :param : IA_diamant:                  [IA_diamant] : class représentant l'IA
    :return: proba_appart_tresor          [float]
    """
    return sum(IA_diamant.manche_deck_pieges.values()) / max(IA_diamant.nb_carte,1)


def proba_appart_danger_fin(IA_diamant):
    """
    Calcule la probabilité qu'une carte danger qui est déjà sur le banc sorte au prochain tour
    :param : IA_diamant:                  [IA_diamant] : class représentant l'IA
    :return: proba_appart_danger_fin      [float]
    """
    proba = 0

    for danger in IA_diamant.liste_dangers_banc:
        proba += IA_diamant.manche_deck_pieges[danger] / max(IA_diamant.nb_carte,1)

    return proba / max(len(IA_diamant.liste_dangers_banc), 1)

def ratio_tresor_reste_possible(IA_diamant):
    """
        Calcule la valeur moyenne des cartes trésor qu'ils restent dans le deck
        :param : IA_diamant:                  [IA_diamant] : class représentant l'IA
        :return: ratio_tresor_reste_possible  [float]
        """
    return sum(IA_diamant.manche_deck_tresors) / max(len(IA_diamant.manche_deck_tresors),1)

def compte_danger(IA_diamant):
    """
        Comptabilise le nombre de danger sur le banc et y retire le nombre de danger qui n'ont plus d"impact sur la partie,
        car il y a plus assez exemplaire dans le deck
        :param IA_diamant:
        :return:nb_dangers_banc               [int]
        """
    nb_dangers_banc = len(IA_diamant.liste_dangers_banc)

    for danger in IA_diamant.liste_dangers_banc:
        if IA_diamant.liste_dangers_elimine_jeu.count(danger) == 2:
            # Ce danger ne peut plus provoqué d'accident, il n'y a pas de deuxième carte
            nb_dangers_banc -= 1

    return nb_dangers_banc

def majReseau(individuDePicsou: INDIVIDU, Picsou: Joueur_X8, IA_diamant, tour):
    """
    Met à jour les différents neuronnes d'entrée par rapport à l'état actuel du jeu
    :param individuDePicsou:
    :param Picsou:
    :param IA_diamant:
    :param tour:
    :return: None
    """

    devine_valeur(tour, IA_diamant, False)  # On prend en compte le tour

    # mise à jour des inputs
    # info partie
    #individuDePicsou.lesNeurones[0].valeur = IA_diamant.nb_manche_partie  # nb de manche en tout dans la partie
    #individuDePicsou.lesNeurones[1].valeur = len(IA_diamant.l_joueurs)  # nb de joueur dans la partie

    # info Joueur Picsou
    individuDePicsou.lesNeurones[0].valeur = Picsou.inv_manche  # nb de diamant dans la manche en cours
    # individuDePicsou.lesNeurones[1].valeur = Picsou.inv_partie  # je sais pas si utile puisqu'on a le score
    individuDePicsou.lesNeurones[1].valeur = compte_danger(IA_diamant)
    #individuDePicsou.lesNeurones[4].valeur = Picsou.inv_relique  # nb de relique posséder dans la partie

    # info manche
    #individuDePicsou.lesNeurones[5].valeur = IA_diamant.no_tour  # numéro du tour actuel
    individuDePicsou.lesNeurones[2].valeur = IA_diamant.reste_tresor  # reste du trésor dans la manche actuelle
    individuDePicsou.lesNeurones[3].valeur = IA_diamant.nb_carte  # nb carte restant actuellement dans le deck
    #individuDePicsou.lesNeurones[8].valeur = IA_diamant.no_manche  # numéro de la manche actuelle

    # probabilité de sortie de carte
    individuDePicsou.lesNeurones[4].valeur = proba_appart_tresor(
        IA_diamant)  # probabilité qu'une carte trésor sorte le prochain tour
    individuDePicsou.lesNeurones[5].valeur = proba_appart_relique(
        IA_diamant)  # probabilité qu'une carte relique sorte le prochain tour
    individuDePicsou.lesNeurones[6].valeur = proba_appart_danger(
        IA_diamant)  # probabilité qu'une carte danger sorte le prochain tour
    individuDePicsou.lesNeurones[7].valeur = proba_appart_danger_fin(
        IA_diamant)  # probabilité qu'une carte danger déjà présente sur le banc sorte le prochain tour
    individuDePicsou.lesNeurones[8].valeur = ratio_tresor_reste_possible(IA_diamant)


def feedForward(individuDePicsou: INDIVIDU):
    """
    :principe :
        On fait les calculs des connexions afin de déduire à la fin la valeur du neurone lier à la décision de partir.


        On met à jour les neurones cachés ainsi que le neurone de décision.
    :param :
        individuDePicsou            INDIVIDU : Le réseau de neurone de Picsou
    :return:
        None

    Note : Basé sur le travail du vidéaste Laupok.
    """

    # On réinitialise les neurones de sortie de chaque connexion vu qu'ils vont récupérer les
    # différents résultats des différents calculs.

    # Un neurone de sortie peut être un neurone cacher ou un neurone de décision (neurone OUTPUT)

    for connexion in individuDePicsou.lesConnexions:

        if connexion.actif:
            # Si la connexion est active dans le réseau,
            # C'est-à-dire qu'on a pas du la remplacer par deux nouvelles connexions à cause de l'ajout d'un neurone (en résumé).

            individuDePicsou.lesNeurones[connexion.sortie].valeur = 0

    for connexion in individuDePicsou.lesConnexions:
        # On prend le neurone d'entrée et de sortie de la connexion

        neuroneEntree = connexion.entree  # ce sont des int pour les deux
        neuroneSortie = connexion.sortie

        if connexion.actif:
            # Si la connexion est active, alors on multiplie la valeur du neurone d'entrée par le poids.
            # Cependant, le neurone de sortie peut déjà comporter d'autres calculs d'autres connexions s'il
            # est également neurone de sortie de d'autres connexions.

            # Donc on ajoute à la valeur du neurone de sortie notre calcul.
            calcul = individuDePicsou.lesNeurones[neuroneEntree].valeur * connexion.poids
            individuDePicsou.lesNeurones[neuroneSortie].valeur += calcul

            # Un poids permet de réajuster une valeur d'un neurone d'entrée.
            # Ainsi, un neurone d'entrée peut plus ou moins compter dans le résultat mis dans le neurone de sortie.
            # Le rôle du poids de la connexion est décrite ici de manière très brève.


def priseDeDecision(individuDePicsou):
    """
    :principe :
        C'est ici que nous allons prendre la décision de rester ou de partir en fonction de la valeur du neurone d'OUTPUT.
    :param :
        individuDePicsou        INDIVIDU : Le réseau de neurones de Picsou
    :return:
                                    STR  : 'R'  → L'IA aimerait bien partir
                                           'X'  → On aimerait rester
    """

    # On récupère la valeur du neurone d'OUTPUT, celui qui comporte le résultat final de tous les calculs.
    # Donc le neurone qui correspond à la prise de décision de l'intelligence artificielle.

    valeurDeDecisionSortir = individuDePicsou.lesNeurones[NB_INPUT + NB_OUTPUT - 2].valeur  # Neurone Partir
    valeurDeDecisionRester = individuDePicsou.lesNeurones[NB_INPUT + NB_OUTPUT - 1].valeur  # Neurone rester

    #assert 2==1, str(valeurDeDecisionSortir)+" /// "+str(valeurDeDecisionRester)

    #print("Valeur de décision:",valeurDeDecision,"\n")

    #
    # Permet d'avoir un résultat toujours inférieur à 1.
    resultatSortir = valeurDeDecisionSortir / (1 + abs(valeurDeDecisionSortir))  # Calcul venant du vidéaste Laupok
    resultatRester = valeurDeDecisionRester / (1 + abs(valeurDeDecisionRester))

    #resultatSortir = valeurDeDecisionSortir / (1 + abs(valeurDeDecisionSortir))
    #resultatRester = 0.5


    if resultatSortir > resultatRester:
        return 'R'
    else:
        return 'X'