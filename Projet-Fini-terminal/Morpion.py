# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

def tour_suivant(tour):
    """ Cette fonction permet de changer de tour, notre tour correspond au joueur qui joue, le joueurs dépend de la liste [X,O] liste de deux éléments
        Pour simplifier la chose nous voulons que tour soit toujours soit 0 soit 1, pour fonctionner avec la fonction joueur.
        Cette fonction passe de 0 à 1 et de 1 à 0"""
    tour += 1
    tour = tour % 2
    return tour

def partie_gagnee(table):
    """ Cette fonction vérifie simplement si la partie est finie ou non.
        Pour cela elle vérifie si les trois élément d'une ligne, colone ou diagonale sont les mêmes."""
    # Vérification alignement horizontal
    if table[0] == table[1] and table[1] == table[2]:
        return table[0]
    elif table[3] == table[4] and table[4] == table[5]:
        return table[3]
    elif table[6] == table[7] and table[7] == table[8]:
        return table[6]
    # Vérification alignement verticale
    elif table[0] == table[3] and table[3] == table[6]:
        return table[0]
    elif table[1] == table[4] and table[4] == table[7]:
        return table[1]
    elif table[2] == table[5] and table[5] == table[8]:
        return table[2]
    # Vérification alignement diagonal
    elif table[0] == table[4] and table[4] == table[8]:
        return table[0]
    elif table[2] == table[4] and table[4] == table[6]:
        return table[2]
    else :
        return False
    
def partie_gagnable(table):
    """ Crée un dictionnaire qui à pour clé le signe et pour valeur l'emplacement ou il y a une vicroire possible"""
    emplacement={}
    # Vérification alignement horizontal
        # Ligne 1
    if table[0] == table[1]:
        emplacement[table[0]] = 2
    elif table[1] == table[2]:
        emplacement[table[1]] = 0
    elif table[0] == table[2] :
        emplacement[table[0]] = 1
        # Ligne 2
    if table[3] == table[4] :
        emplacement[table[3]] = 5
    elif table[4] == table[5] :
        emplacement[table[4]] = 3
    elif table[3] == table[5]:
        emplacement[table[3]] = 4
        # Ligne 3  
    if table[6] == table[7]:
        emplacement[table[6]] = 8
    elif table[7] == table[8]:
        emplacement[table[7]] = 6
    elif table[6] == table[8]:
        emplacement[table[6]] = 7 
    # Vérification alignement verticale
        # Colonne 1
    if table[0] == table[3]:
        emplacement[table[0]] = 6
    elif table[3] == table[6]:
        emplacement[table[3]] = 0
    elif table[0] == table[6] :
        emplacement[table[0]] = 3
        # Colonne 2
    if table[1] == table[4] :
        emplacement[table[1]] = 7
    elif table[4] == table[7] :
        emplacement[table[4]] = 1
    elif table[1] == table[7]:
        emplacement[table[1]] = 4
        # Ligne 3  
    if table[2] == table[5]:
        emplacement[table[2]] = 8
    elif table[5] == table[8]:
        emplacement[table[5]] = 2
    elif table[2] == table[8]:
        emplacement[table[2]] = 5
    
    # Vérification alignement diagonal
        # De 0 à 8 
    if table[0] == table[4]:
        emplacement[table[0]] = 8
    elif table[4] == table[8]:
        emplacement[table[4]] = 0
    elif table[0] == table[8] :
        emplacement[table[0]] = 4
        # De 6 à 2
    if table[6] == table[4] :
        emplacement[table[6]] = 2
    elif table[4] == table[2] :
        emplacement[table[4]] = 6
    elif table[6] == table[2]:
        emplacement[table[6]] = 4

def coup_jouable(table, emplacement):
    """ Cette fonction permet de vérifier si la case est libre ou non.
        Pour cela on vérifie si l'emplacement de la demande de l'utilisateur correspond bien a son nombre.
        Par exemple : l'utilisateur demande a jouer sur la case 2 on va vérifier dans la liste à l'emplacement 2 ( table[2-1] ) car les listes commencent à 0
        On vérifie si la valeur de cet emplacement est bien égale à l'emplacement demandé, si sur la case 2 c'est bien un 2"""
    return table[emplacement-1] == str(emplacement)

def affichage(table):
    """ Cette fonction n'est présente que pour éviter de recopier ce print à chaque fois"""
    print("-------\n",table[0],table[1],table[2],"\n",table[3],table[4],table[5],"\n",table[6],table[7],table[8])

def jeu_duo():
    """ Cette fonction est la fonction du jeu, c'est celle qui permet le fonctionement du programme."""
    table = ["1","2","3","4","5","6","7","8","9"]
    tour = 0
    joueurs = ["X","O"]
    partie_fini = "False"
    coup = 9    # Correspond au nombre de case libre
    while partie_fini != True :
        affichage(table)
        p = eval(input("Sur quelle case voulez vous jouer ( C'est au joueur " + joueurs[tour] + " de jouer )"))
        if p > 0 and p < 10:    # Vérifie si le coup est entre 1 et 9 compris, car il n'y a que 9 cases disponible
            if coup_jouable(table, p):
                table[p-1] = joueurs[tour]  # L'emplacement joué devient le symbole du joueur
                coup -= 1
                if partie_gagnee(table) != False :  # La fonction partie_gagnee renvoie le symbole du vainqueur, donc je vérifie si elle retourne un autre élement que False
                    affichage(table)
                    partie_fini = True  # Ceci me permettra de ne pas rentrer dans mon while
                    print("\n \n Bravo au joueur",joueurs[tour], "tu as humilié ton adversaire !")
                elif coup ==  0:    # Si il n'y a plus de coup cela signifie que toute la table est remplie, comme il n'y a pas eu de gagnant avant il y a égalitée
                    affichage(table)
                    partie_fini = True
                    print("\n \n C'est un égalité.")
                else :
                    tour = tour_suivant(tour)   #   Si il n'y a pas de vainqueur et qu'il n'y a pas égalité cela veut dire que la partie n'est pas finis
            else :
                print("Coup injouable recommence et concentre toi !")
        else :
            print("Votre emplacement est invalide")
            
def ordi(table, tour, coup_jouer):
    d = partie_gagnable(table)
    if d != None :
        if 'O' in d :
            return d['O']
        else :
            return d['X']
    if tour == 0:
        return 0
    if tour == 1 :
        if 

def jeu_solo():
    """ Cette fonction est la fonction du jeu, c'est celle qui permet le fonctionement du programme."""
    table = ["1","2","3","4","5","6","7","8","9"]
    coup_jouer = []
    tour = 0
    joueurs = ["X","O"]
    partie_fini = "False"
    coup = 9    # Correspond au nombre de case libre
    while partie_fini != True :
        affichage(table)
        p = eval(input("Sur quelle case voulez vous jouer ( C'est au joueur " + joueurs[tour] + " de jouer )"))
        if p > 0 and p < 10:    # Vérifie si le coup est entre 1 et 9 compris, car il n'y a que 9 cases disponible
            if coup_jouable(table, p):
                table[p-1] = joueurs[tour]  # L'emplacement joué devient le symbole du joueur
                coup -= 1
                coup_jouer.append(p-1)
                if partie_gagnee(table) != False :  # La fonction partie_gagnee renvoie le symbole du vainqueur, donc je vérifie si elle retourne un autre élement que False
                    affichage(table)
                    partie_fini = True  # Ceci me permettra de ne pas rentrer dans mon while
                    print("\n \n Bravo au joueur",joueurs[tour], "tu as humilié ton adversaire !")
                elif coup ==  0:    # Si il n'y a plus de coup cela signifie que toute la table est remplie, comme il n'y a pas eu de gagnant avant il y a égalitée
                    affichage(table)
                    partie_fini = True
                    print("\n \n C'est un égalité.")
                else :
                    tour = tour_suivant(tour)   #   Si il n'y a pas de vainqueur et qu'il n'y a pas égalité cela veut dire que la partie n'est pas finis
            else :
                print("Coup injouable recommence et concentre toi !")
        else :
            print("Votre emplacement est invalide")