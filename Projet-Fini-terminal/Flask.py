from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

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
    if table[0] == table[1] and table[1] == table[2] and table[0] != "":
        return table[0]
    elif table[3] == table[4] and table[4] == table[5] and table[3] != "":
        return table[3]
    elif table[6] == table[7] and table[7] == table[8] and table[6] != "":
        return table[6]
    # Vérification alignement verticale
    elif table[0] == table[3] and table[3] == table[6] and table[0] != "":
        return table[0]
    elif table[1] == table[4] and table[4] == table[7] and table[1] != "":
        return table[1]
    elif table[2] == table[5] and table[5] == table[8] and table[2] != "":
        return table[2]
    # Vérification alignement diagonal
    elif table[0] == table[4] and table[4] == table[8] and table[0] != "":
        return table[0]
    elif table[2] == table[4] and table[4] == table[6] and table[2] != "":
        return table[2]
    else :
        return False

def coup_jouable(table, emplacement):
    """ Cette fonction permet de vérifier si la case est libre ou non.
        Pour cela on vérifie si l'emplacement de la demande de l'utilisateur correspond bien a son nombre.
        Par exemple : l'utilisateur demande a jouer sur la case 2 on va vérifier dans la liste à l'emplacement 2 ( table[2-1] ) car les listes commencent à 0
        On vérifie si la valeur de cet emplacement est bien égale à l'emplacement demandé, si sur la case 2 c'est bien un 2"""
    if table[emplacement-1] == "":
        return True 
    else: 
        return False
            

@app.route('/')
def acceuil():
    """ Cette fonction permet de définir des variables plutôt importante et permet d'afficher mon site d'acceuil."""
    global liste, tour, joueurs, partie_fini, coup
    liste = ["","","","","","","","",""]    # C'est la grille de jeu
    tour = 0
    joueurs = ["X","O"]
    partie_fini = "False"
    coup = 9    # Correspond au nombre de case libre
    return render_template('duo.html') 

@app.route('/jeu-duo',  methods = ['GET'])
def jeu():
    """ Cette fonction permet de jouer au morpion """
    global liste, tour, coup, partie_fini, iddj
    
    connexion = sqlite3.connect('database.db')  # Connexion avec ma base de donnée 
    curseur = connexion.cursor()
    
    # Récupère les noms des personnes qui ont déjà joué
    requete = "SELECT pseudo FROM stats"
    ##Pour repèrer les lignes renvoyées
    curseur.execute(requete)    
    ##Pour récupérer les lignes
    lignes1 = curseur.fetchall()
    nom = []
    for i in lignes1 :
        """ Ceci me permet d'avoir une liste avec les pseudo seuls, car les lignes au dessus me renvoient des tuples """
        name = i[0] 
        name = name.strip()
        nom.append(name)
        
    # Récupère les statistiques présentent dans la table sous forme de dictionaire 
    requete = "SELECT * FROM stats"
    ##Pour repèrer les lignes renvoyées
    curseur.execute(requete)
    ##Pour récupérer les lignes
    lignes = curseur.fetchall()
    stats = {}
    for i in lignes:
        """ Permet d'obtenir un dictionaire avec pour clé le pseudo et pour valeur les statistique du joueur"""
        stats[i[0]] = list(i[1:])
               
        result = request.args   # Récupère les données entrées sur le site 
    if coup == 9:
        iddj = [result["croix"],result["rond"]] # Défini le nom des joueurs 
        for i in range(len(iddj)):
            if len(iddj[i]) > 2 : 
                iddj[i] = iddj[i][0].upper() + iddj[i][1:].lower()  # On met la forme du pseudo sous la première lettre en majuscule et les autres en minuscule pour pas qu'il y ai de soucis dans ma base de donnnée 
                
                if iddj[i] not in nom:  # Si un des joueurs n'est pas dans ma base de donnée 
                    curseur.execute('''INSERT INTO stats (pseudo,partie_jouee,partie_gagnee,egalitee,partie_perdue) VALUES ("'''+iddj[i]+'''",0,0,0,0)''')  # Cette ligne permet d'ajouter le joueur dans ma base de donnée 
                    connexion.commit()  # J'enregistre les modification dans la base de donnée 
                    stats[iddj[i]] = '(0,0,0,0)'    # J'ajoute dans mon dictinaire les stats qui sont nul car première partie du joueur
            else :
                if i == 0 : 
                    iddj[i] = "Croix"   # Si il n'y a pas de pseudo défini nous jourons sous les noms croix et/ou rond 
                else :
                    iddj[i] = "Rond"
                    
    while partie_fini != True :
        p = int(result['bouton'])   # Récupère l'emplacement sur lequel on a joué 
        if coup_jouable(liste, p) == False:
            return render_template("jeu.html", un = liste[0], deux = liste[1], trois = liste[2], 
                        quatre = liste[3], cinq = liste[4], six = liste[5], sept = liste[6],
                        huit = liste[7], neuf = liste[8])   # Comme le coup est injouable on affiche simplement la grille sans rien changé ce qui permet au même joueur de rejouer 
        
        elif coup_jouable(liste, p) == True:
            liste[p-1] = joueurs[tour]  # L'emplacement joué devient le symbole du joueur
            coup -= 1
            
            if partie_gagnee(liste) != False :  # La fonction partie_gagnee renvoie le symbole du vainqueur, donc je vérifie si elle retourne un autre élement que False
                partie_fini = True  # Ceci me permettra de ne pas rentrer dans mon while
                
                # On ajoute une partie joué pour les deux joueurs
                stats[iddj[tour]][0] += 1  
                stats[iddj[tour-1]][0] += 1 
                # On ajoute une victoire pour le vainqueur et une défaite pour l'autre 
                stats[iddj[tour]][1] += 1  
                stats[iddj[tour-1]][3] += 1 
                # On modifie la base de donnée 
                curseur.execute('UPDATE stats SET (partie_jouee,partie_gagnee,egalitee,partie_perdue) = '+str(tuple(stats[iddj[tour]]))+' WHERE pseudo ="'+iddj[tour]+'"')
                curseur.execute('UPDATE stats SET (partie_jouee,partie_gagnee,egalitee,partie_perdue) = '+str(tuple(stats[iddj[tour-1]]))+' WHERE pseudo ="'+iddj[tour-1]+'"')
                # On enregistre les modifiacations
                connexion.commit()
                # Deconnexion de la base de données
                connexion.close()
                return render_template("fin.html", un = liste[0], deux = liste[1], trois = liste[2], 
                       quatre = liste[3], cinq = liste[4], six = liste[5], sept = liste[6],
                       huit = liste[7], neuf = liste[8], text = " Bravo au joueur "+iddj[tour]+" ( "+joueurs[tour]+" ) tu as humilié ton adversaire !", Jcroix = iddj[0], JcroixP = stats[iddj[0]][0], JcroixV = stats[iddj[0]][1], JcroixE = stats[iddj[0]][2], JcroixD = stats[iddj[0]][3]
                                   ,Jrond = iddj[1], JrondP = stats[iddj[1]][0], JrondV = stats[iddj[1]][1], JrondE = stats[iddj[1]][2], JrondD = stats[iddj[1]][3])
            
            elif coup ==  0:    # Si il n'y a plus de coup cela signifie que toute la table est remplie, comme il n'y a pas eu de gagnant avant il y a égalitée
                partie_fini = True
                
                # On ajoute une partie joué pour les deux joueurs
                stats[iddj[0]][0] += 1  
                stats[iddj[1]][0] += 1 
                # On ajoute une égalitée pour les deux joueurs 
                stats[iddj[0]][2] += 1  
                stats[iddj[1]][2] += 1 
                # On modifie la base de donnée 
                curseur.execute('UPDATE stats SET (partie_jouee,partie_gagnee,egalitee,partie_perdue) = '+str(tuple(stats[iddj[0]]))+' WHERE pseudo ="'+iddj[0]+'"')
                curseur.execute('UPDATE stats SET (partie_jouee,partie_gagnee,egalitee,partie_perdue) = '+str(tuple(stats[iddj[1]]))+' WHERE pseudo ="'+iddj[1]+'"')            
                connexion.commit()
                ## Deconnexion de la base de données
                connexion.close()
                return render_template("fin.html", un = liste[0], deux = liste[1], trois = liste[2], 
                       quatre = liste[3], cinq = liste[4], six = liste[5], sept = liste[6],
                       huit = liste[7], neuf = liste[8], text = "C'est un égalité.", Jcroix = iddj[0], JcroixP = stats[iddj[0]][0], JcroixV = stats[iddj[0]][1], JcroixE = stats[iddj[0]][2], JcroixD = stats[iddj[0]][3]
                                   ,Jrond = iddj[1], JrondP = stats[iddj[1]][0], JrondV = stats[iddj[1]][1], JrondE = stats[iddj[1]][2], JrondD = stats[iddj[1]][3])
            else :
                tour = tour_suivant(tour)   #   Si il n'y a pas de vainqueur et qu'il n'y a pas égalité cela veut dire que la partie n'est pas finis
            
    if partie_fini == True:
        
                return render_template("fin.html", un = liste[0], deux = liste[1], trois = liste[2], 
                       quatre = liste[3], cinq = liste[4], six = liste[5], sept = liste[6],
                       huit = liste[7], neuf = liste[8], text = "Partie finie, arrête de forcer.", Jcroix = iddj[0], JcroixP = stats[iddj[0]][0], JcroixV = stats[iddj[0]][1], JcroixE = stats[iddj[0]][2], JcroixD = stats[iddj[0]][3]
                                   ,Jrond = iddj[1], JrondP = stats[iddj[1]][0], JrondV = stats[iddj[1]][1], JrondE = stats[iddj[1]][2], JrondD = stats[iddj[1]][3])        
if __name__ == '__main__':
    app.run(debug = True, use_reloader = False)