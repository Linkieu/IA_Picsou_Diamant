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