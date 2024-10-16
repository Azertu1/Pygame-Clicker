import random
from random import choice, randint
import mysql.connector
import pygame
import sys
from pygame.locals import *

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Connection au serveur MySQL>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

mydb = mysql.connector.connect(
  host="88.166.8.244",
  user="user",
  password="",
  database="clicker"
)

mycursor = mydb.cursor()

pygame.init()

clock = pygame.time.Clock()

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Définition des variables>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Serveur Clicker")
fenetre_rect = fenetre.get_rect()

perso = pygame.image.load("F:\Pygame\perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso.topleft = (200,300)

multi=10
a=1
b=1
i=90
frequence=45
seconde=30
temps=seconde*30
pause=False
templist=[]
tempsclic=0

# TODO: Système de lecture des coordonées des clic depuis une table [position_clic : id_joueur(INT), x(INT), y(INT)], verification et ajout de points dans une table [score : id_joueur(INT), score(INT)]
# TODO: Ajout d'un système anticheat (anti spam clic, anti modification BDD score par joueur, vérification des coordonées clic (si les coordonées relatives du clic par rapport à la cible sont toujours les même)
# TODO: Terminer le système de parties (côté client aussi)

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[BOUCLE DE JEU]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

while True :

    clock.tick(30)
    i-=1

    if not(pause):
        temps-=1
        mycursor.execute(str("UPDATE sync SET chrono ="+str(temps)))
        mydb.commit()

    #<<<<<<<<<<<<<<<<<<<<<<<<Système de pause de partie (un peu inutile maintenant, à modifier)>>>>>>>>>>>>>>>>>>>>>>>>

    #RÉSIDU DE L'ANCIEN SYSTEME DE COORDONÉS, IL A CHANGÉ DEPUIS, NE PAS TROP FAIRE ATTENTION (il peut quand même peut être vous servir)
    #La pause toute les x secondes permetait de synchroniser les position de tout les client connectés en reglant l'élément "go" du tableau SQL à 1. Cela déplace instantanément les cibles à des coordonées prédéfinies (identique dans les clients et le serveur)
    if pause:
        if i<=0:
            mycursor.execute("UPDATE score SET score=0 WHERE score>1")
            mydb.commit()
            pause=False
            i=45
            print("unpause")


    if temps<=0:
        mydb.commit()
        temps=seconde*30
        position_perso.topleft = (200,300)
        pause=True
        i=135
        print("pause")

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Permet de quitter le programe>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    for event in pygame.event.get() :

        if event.type == QUIT :
            pygame.quit()
            sys.exit()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Système de score>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    mycursor.execute("SELECT * FROM position_joueur")
    clics = mycursor.fetchall()
    mydb.commit()

    for joueur in clics:
        x=joueur[1]
        y=joueur[2]
        tempsclic=joueur[3]
    #Vérifie que les coordonnées du clic sont dans la hitbox de la cible (l'anticheat se placera sûrement par ici)
        if (tempsclic==temps-10 or tempsclic<temps+10) and position_perso.left <= x <= position_perso.left + position_perso.width and y >= position_perso.top and y <= position_perso.top + position_perso.height:
    #Récupère le score actuel du joueur
            mycursor.execute("SELECT * FROM score WHERE id_joueur = "+str(joueur[0]))
            point = mycursor.fetchall()
            mydb.commit()
            point=point[0][1]
            point+=1
    #Met à jour le score du joueur
            mycursor.execute("UPDATE score SET score= "+str(point)+" WHERE id_joueur="+str(joueur[0]))
            mydb.commit()

    mycursor.execute("UPDATE position_joueur SET x=0, y=0, temps=0")
    mydb.commit()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Algorithme de déplacement>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #PARTIE NON ALÉATOIRE DU CODE Calcul du "Rebond" de la cible contre les limite de l'arène
    if position_perso.left>=700:
        a=0-1*multi

    elif position_perso.left<=100:
        a=1*multi

    if position_perso.top>=500:
        b=0-1*multi

    elif position_perso.top<=100:
        b=1*multi
    #PARTIE ALÉATOIRE DU CODE Mise à jour des instruction de déplacement  dans le tableau SQL ( par une valaur aléatoire une fois toute les 45 itérations)
    #Toutes ces conditions servent à éviter que le personage soit immobile ou + lent (dans l'évantualité que random choisisse un déplacement de 0 pour x ou y)
    elif not(pause):
        if i<=0:
            a=random.choice([-1,-1,0,1,1])*multi
            if a==0:

                b = random.choice([-2, 2]) * multi
            else:
                b=random.choice([-1,-1,0,1,1])*multi
                if b==0:
                    a = random.choice([-2, 2]) * multi
            i=frequence
        else:
            pass
    #*voir explications de la pause plus haut* instruction de déplacement nulle pendant la pause (les cibles reste fixe pendant une itération)
    elif pause:
            a=0
            b=0
    #Mise à jour de la position de la cible dans le tableau "position_cible"
    position_perso = position_perso.move(a,b)

    mycursor.execute(str("UPDATE position_cible SET x = " + str(position_perso[0]) + " WHERE id_cible = 1"))
    mydb.commit()
    mycursor.execute(str("UPDATE position_cible SET y = " + str(position_perso[1]) + " WHERE id_cible = 1"))
    mydb.commit()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<Affichage des déplacement de la cible côté serveur (pour debug)>>>>>>>>>>>>>>>>>>>>>>>>>

    font = pygame.font.SysFont(None, 48)
    nom = font.render("Serveur Clicker 2", True, "green")

    fond = pygame.Surface((800, 600))
    fond.fill((255, 186, 181))
    fond = fond.convert()

    #DÉMO !
    #mycursor.execute("SELECT * FROM score ")
    #leaderboard = mycursor.fetchall()
    #mydb.commit()
    #font = pygame.font.SysFont(None, 24)
    #score= font.render("Client 1 : " + str(leaderboard[0][1]), True, "blue")

    #font = pygame.font.SysFont(None, 24)
    #score2 = font.render("Client 2 : " + str(leaderboard[1][1]), True, "blue")
    # DÉMO !

    fenetre.blit(fond, fenetre_rect)
    fenetre.blit(perso, position_perso)
    fenetre.blit(nom, (270, 40))
    #fenetre.blit(score, (80, 80))
    #fenetre.blit(score2, (80, 120))

    pygame.display.flip()