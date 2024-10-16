import mysql.connector
import pygame, sys
from random import *
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
pygame.display.set_caption("Client Clicker")
fenetre_rect = fenetre.get_rect()

perso = pygame.image.load("F:\Pygame\perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso.topleft = (200,300)

viseur = pygame.image.load("F:\Pygame\pointeur.png").convert_alpha()
position_viseur = viseur.get_rect()
position_viseur.topleft = pygame.mouse.get_pos()

multi=10
a=1
b=1
i=90
seconde=30
temps=seconde*30
chrono=temps/30
frequence=45
go=0
id=randint(0,999999999)

mycursor.execute("INSERT INTO position_joueur VALUES (%s, %s, %s, %s)", (id, 0, 0, 0))
mydb.commit()

mycursor.execute("INSERT INTO score VALUES (%s, %s)", (id, 0))
mydb.commit()

# TODO: Système de détection de clic et écriture des coordonées du clic dans une table [position_clic : id_joueur(INT), x(INT), y(INT)]
# TODO: Terminer le système de parties (côté serveur aussi)
# TODO: Faire une interface complete (qui affiche "partie déjà en cours" quand la table SQL go =1 et qui montre un leaderboard à la fin)

# [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[BOUCLE DE JEU]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

while True :
    clock.tick(30)
    mycursor.execute("SELECT chrono FROM sync")
    temps = mycursor.fetchall()
    mydb.commit()
    chrono = temps[0][0] // 30

    # <<<<<<<<<<<<<<<<<<<<<<<<Système de pause de partie (un peu inutile maintenant, à modifier)>>>>>>>>>>>>>>>>>>>>>>>>

    # RÉSIDU DE L'ANCIEN SYSTEME DE COORDONÉS, IL A CHANGÉ DEPUIS, NE PAS TROP FAIRE ATTENTION (il peut quand même peut être vous servir)
    #vérification de l'élément "go" (si go==1 alors la cible va vers des coordonées prédifinies en même temps que celle du serveur afin de synchroniser les éléments)
    if temps==0:
        position_perso.topleft = (200,300)
        temps=seconde*30
    i-=1

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Permet de quitter le programe>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    for event in pygame.event.get() :
        if event.type == QUIT :
            mycursor.execute("DELETE FROM position_joueur WHERE id_joueur="+str(id))
            mydb.commit()
            mycursor.execute("DELETE FROM score WHERE id_joueur=" + str(id))
            mydb.commit()
            pygame.quit()
            sys.exit()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Système de clics>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Envoie des coordonnées x y du clic dans la table position_joueur
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            mycursor.execute("UPDATE position_joueur SET x="+str(x)+" WHERE id_joueur="+str(id))
            mydb.commit()
            mycursor.execute("UPDATE position_joueur SET y=" + str(y) + " WHERE id_joueur=" + str(id))
            mydb.commit()
            mycursor.execute("UPDATE position_joueur SET temps=" + str(temps[0][0]) + " WHERE id_joueur=" + str(id))
            mydb.commit()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Système de score>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    mycursor.execute("SELECT score FROM score WHERE id_joueur=" + str(id))
    points = mycursor.fetchall()
    mydb.commit()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Déplacement de la cible>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #mise à jour des instruction de déplacement (à chaque itération)
    mycursor.execute("SELECT * FROM position_cible WHERE id_cible=1")
    myresult = mycursor.fetchall()
    mydb.commit()
    position_perso = myresult[0][1], myresult[0][2]

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Affichage des éléments>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    x, y = pygame.mouse.get_pos()
    position_viseur.topleft = x - 50, y - 50

    font = pygame.font.SysFont(None, 24)
    chronometre = font.render("Chrono : " + str(chrono) + " s", True, "blue")

    font = pygame.font.SysFont(None, 48)
    nom = font.render("Client Clicker 2", True, "green")

    font = pygame.font.SysFont(None, 24)
    score= font.render("Score : " + str(points[0][0]), True, "blue")

    font = pygame.font.SysFont(None, 48)
    pause = font.render("Pause d'interpartie", True, "green")

    fond = pygame.Surface((800, 600))
    fond.fill((10, 186, 181))
    fond = fond.convert()

    fenetre.blit(fond, fenetre_rect)
    fenetre.blit(nom, (280, 40))

    if temps[0][0] > 0:
        fenetre.blit(perso, position_perso)
        fenetre.blit(viseur, position_viseur)
        fenetre.blit(chronometre, (630, 80))
        fenetre.blit(score, (80, 80))

    if temps[0][0] == 0:
        fenetre.blit(pause, (250, 80))

        mycursor.execute("SELECT id_joueur,score FROM score ORDER BY score DESC")
        leaderboard = mycursor.fetchall()
        mydb.commit()

        for i in range(len(leaderboard)):
            if leaderboard[i][0]==id:
                place=i+1

        font = pygame.font.SysFont(None, 36)
        gagnanthud = font.render("Gagnant : id" + str(leaderboard[0][0]) + " avec un score de : " + str(leaderboard[0][1]), True, "white")
        if place==1:
            font = pygame.font.SysFont(None, 52)
            placehud = font.render("Vous avez gagné !", True, "yellow")
        else:
            font = pygame.font.SysFont(None, 36)
            placehud = font.render("Vous êtes arrivé " + str(place) + "e !", True, "white")

        fenetre.blit(gagnanthud, (150, 200))
        fenetre.blit(placehud, (150, 250))

    pygame.display.flip()