#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 12:22:15 2023

@author: matthieu
"""
import pickle

def recup_individu(nom_fichier, chemin):
    f = open(chemin + nom_fichier, "rb")
    individu_charger = pickle.load(f)
    f.close()

    return individu_charger

def SAVE_DESCRIPTIF(desc, chemin, nom_fichier):
    # voir https://python.doctor/page-lire-ecrire-creer-fichier-python
    # nom_f = "RAPPORT.txt"
    nom_f = "DESCRIPTIF_" + nom_fichier + '.txt'

    if type(desc) == str:

        fichier = open(chemin + nom_f, "w")  # Note: mettre a pour Ouvre en Ã©criture Ã  la suite le fichier
        fichier.write("\n" + desc)  # Ãcrit dans le fichier, Ã  la suite
        fichier.close()  # Ferme le fichier

        print("SAUVEGARDE >> Le fichier " + nom_f + " a bien Ã©tÃ© sauvegardÃ© !")
    elif type(desc) == list:
        fichier = open(chemin + nom_f, "w")
        for ligne in desc:
            if type(ligne) == str:
                fichier.write("\n" + ligne)
        fichier.close()

        print("SAUVEGARDE >> Le fichier " + nom_f + " a bien Ã©tÃ© sauvegardÃ© !")
    else:
        print("ERREUR : IMPOSSIBLE DE SAUVEGARDER")


class NEURONE:
    # CrÃ©er un neurone vide
    # Note : InspirÃ© du travail du vidÃ©aste Laupok.

    def __init__(self):
        self.valeur = 0  # Valeur du neurone par dÃ©faut
        self.id = -1  # Id par dÃ©faut d'un neurone crÃ©er (devra Ãªtre changÃ©).
        self.typeNeurone = ""  # Type de neurone (INPUT, OUTPUT, CACHER)



class CONNEXION:
    def __init__(self):
        self.innovation = 0  # Identifiant unique de la connexion. Indique que c'est l'innovation Ã¨me connexion.
        self.entree = 0  # Neurone d'entrÃ©e
        self.sortie = 0  # Neurone de sortie
        self.actif = True  # Le neurone est actif ou mort
        self.poids = 0  # Poids de la connexion



class INDIVIDU:
    # CrÃ©er un individu vide, c'est-Ã -dire un rÃ©seau de neurone de base.
    # Note : InspirÃ© du travail du vidÃ©aste Laupok.
    def __init__(self):
        self.idEspece = 0  # Identifiant de l'espÃ¨ce oÃ¹ appartient l'individu
        self.nbNeurones = 0  # Le nombre de neurones qui composent l'individu (le rÃ©seau de neurones).
        # en dehors des neurones d'entrÃ©es (INPUT) et de sorties (OUTPUT).
        self.score = 1  # Score qu'a fait l'individu (nombre de diamants +1 de gagnÃ©)
        self.lesNeurones = []  # Liste de tous les neurones de l'individu
        self.lesConnexions = []  # Liste les connexions entre les neurones de l'individu.

        self.nbInnovationConnexions = 0




class ESPECE:
    def __init__(self):
        self.nbEnfants = 0  # Nombre d'individus enfants qu'a faits l'espÃ¨ce
        self.scoreMoyen = 0  # Nombre moyen de diamants que rÃ©colte l'espÃ¨ce par parties
        self.scoreMax = 0  # Nombre maximum de diamants qu'a fait un individu de l'espÃ¨ce.
        self.lesIndividus = []  # Liste des objets individus





#individu = recup_individu("INDIVIDU_PLUS_FORT20230113_22482448943.ind", "")


def affiche_descriptif(nom_fichier, chemin):
    individu = recup_individu(nom_fichier, chemin)
    descriptif = []
    
    descriptif.append("============================================")
    descriptif.append("INFORMATION DE L'INDIVIDU "+nom_fichier)
    descriptif.append("============================================\n")
    
    descriptif.append("idEspece : "+str(individu.idEspece))
    descriptif.append("nbNeurones : "+str(individu.nbNeurones))
    descriptif.append("score : "+str(individu.score))
    descriptif.append("nbInnovationConnexions : "+str(individu.nbInnovationConnexions))
    
    for neurone in individu.lesNeurones:
        descriptif.append("------- NEURONE")
        descriptif.append("        valeur : "+str(neurone.valeur))
        descriptif.append("        id : "+str(neurone.id))
        descriptif.append("        typeNeurone : "+str(neurone.typeNeurone))
        descriptif.append("\n")
    
    descriptif.append("\n\n")
    
    for connexion in individu.lesConnexions:
        if connexion.actif:
            descriptif.append("------- CONNEXION")
            descriptif.append("        innovation : "+str(connexion.innovation))
            descriptif.append("        entree : "+str(connexion.entree))
            descriptif.append("        sortie : "+str(connexion.sortie))
            descriptif.append("        actif : "+str(connexion.actif))
            descriptif.append("        poids : "+str(connexion.poids))
            descriptif.append("\n")
    
    return descriptif, nom_fichier


descriptif = affiche_descriptif("0INDIVIDU_PLUS_FORT20230114_195632765409.ind","MEILLEUR_INDIVIDU/test/bien/")

SAVE_DESCRIPTIF(descriptif[0],"MEILLEUR_INDIVIDU/test/bien/",descriptif[1])
