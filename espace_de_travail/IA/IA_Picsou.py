##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes,
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

from random import *
from PLUS_transformation_info import *
from PLUS_modification_joueurs import *
import time

NB_INPUT = 7  # Nombre de neurones d'entrée
NB_OUTPUT = 2  # Nombre de neurones de sortie


class NEURONE:
    # Créer un neurone vide
    # Note : Inspiré du travail du vidéaste Laupok.

    def __init__(self):
        self.valeur = 0  # Valeur du neurone par défaut
        self.id = -1  # Id par défaut d'un neurone créer (devra être changé).
        self.typeNeurone = ""  # Type de neurone (INPUT, OUTPUT, CACHER)

    def copier(self, neurone_a_copier):
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


# PARTIE : Récupère les infos reçues par le bot et essaye d'en déduire un maximum de valeur


def dec_joueur(info_tour, IA_diamant):
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



def devine_valeur(tour, IA_diamant, preparatif_prochaine_manche):
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



def remise_zero_nv_manche(IA_diamant):
    IA_diamant.remise_zero_nv_manche()
    for joueur in IA_diamant.l_joueurs:
        joueur.remise_zero_joueur_nv_manche()


def proba_appart_tresor(IA_diamant):
    return sum(IA_diamant.manche_deck_tresors) / max(IA_diamant.nb_carte,1)


def proba_appart_relique(IA_diamant):
    return IA_diamant.nb_relique_en_jeu_nn_sortie / max(IA_diamant.nb_carte,1)


def proba_appart_danger(IA_diamant):
    return sum(IA_diamant.manche_deck_pieges.values()) / max(IA_diamant.nb_carte,1)


def proba_appart_danger_fin(IA_diamant):
    proba = 0

    for danger in IA_diamant.liste_dangers_banc:  # Peut-être problème si 2ᵉ danger identique rajouter à liste_dangers_banc
        proba += IA_diamant.manche_deck_pieges[danger] / max(IA_diamant.nb_carte,1)

    return proba / max(len(IA_diamant.liste_dangers_banc), 1)

def ratio_tresor_reste_possible(IA_diamant):
    return sum(IA_diamant.manche_deck_tresors) / max(len(IA_diamant.manche_deck_tresors),1)

def compte_danger(IA_diamant):
    nb_dangers_banc = len(IA_diamant.liste_dangers_banc)

    for danger in IA_diamant.liste_dangers_banc:
        if IA_diamant.liste_dangers_elimine_jeu.count(danger) == 2:
            # Ce danger ne peut plus provoqué d'accident, il n'y a pas de deuxième carte
            nb_dangers_banc -= 1

    return nb_dangers_banc

def majReseau(individuDePicsou: INDIVIDU, Picsou: Joueur_X8, IA_diamant, tour):

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

    """
    if IA_diamant.no_manche > 1:
        # historique de valeur dans les manches
        individuDePicsou.lesNeurones[10].valeur = Picsou.etat_historique.count("M")  # nb de mort du joueur dans la partie
        for i_valeur in range(IA_diamant.nb_manche_partie):
            if Picsou.nb_tour_rester_ds_manche_historique[i_valeur]:
                individuDePicsou.lesNeurones[11 + i_valeur].valeur = Picsou.nb_tour_rester_ds_manche_historique[
                    i_valeur]  # historique des nombres de tours rester pendant les manches
                #individuDePicsou.lesNeurones[14 + IA_diamant.nb_manche_partie * 1 + i_valeur].valeur = \
                #Picsou.inv_historique[i_valeur]  # historique du total de diamant récupéré par manche

                #individuDePicsou.lesNeurones[14 + IA_diamant.nb_manche_partie * 2 + i_valeur].valeur = \
                #Picsou.nb_danger_banc_historique[
                #    i_valeur]  # historique du nombre de dangers sur le banc lorsqu'il est parti
                #individuDePicsou.lesNeurones[14 + IA_diamant.nb_manche_partie * 3 + i_valeur].valeur = \
                #Picsou.nb_reste_tresor_historique[
                #    i_valeur]  # historique du nombre de diamants restant dans le trésor lorsqu'il est parti

    """
def feedForward(individuDePicsou: INDIVIDU):
    """
    P :
        On fait les calculs des connexions afin de déduire à la fin la valeur du neurone lier à la décision de partir.


        On met à jour les neurones cachés ainsi que le neurone de décision.
    E :
        individuDePicsou            INDIVIDU : Le réseau de neurone de Picsou
    S :
        Rien

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
    P :
        C'est ici que nous allons prendre la décision de rester ou de partir en fonction de la valeur du neurone d'OUTPUT.
    E :
        individuDePicsou        INDIVIDU : Le réseau de neurones de Picsou
    S :
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


    #return resultatSortir, resultatRester


class IA_Diamant:
    def __init__(self, match: str, individuDePicsou: INDIVIDU):
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

        self.individuDePicsou = individuDePicsou

        devine_valeur("", self, True)  # On indique à l'IA que c'est une nouvelle manche


        self.test = 50
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

