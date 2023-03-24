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