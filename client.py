import mysql.connector
import pygame, sys
from random import *
from pygame.locals import *


mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="",
  database="clicker"
)

mycursor = mydb.cursor()

pygame.init()

clock = pygame.time.Clock()

#définition des variables

fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Client Clicker")
fenetre_rect = fenetre.get_rect()

perso = pygame.image.load("F:\Pygame\perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso.topleft = (200,300)

multi=10
a=1
b=1
i=90
frequence=45
go=0

while True : # boucle de jeu
    clock.tick(30)

    #vérification de l'élément "go" (si go==1 alors la cible va vers des coordonées prédifinies en même temps que celle du serveur afin de synchroniser les éléments)

    mycursor.execute("SELECT * FROM go")
    myresult = mycursor.fetchall()
    mydb.commit()
    go = myresult[0][0]
    print(go)
    if go==1:
        position_perso.topleft = (200,300)
        go=0

    i-=1

    #Permet de quitter

    for event in pygame.event.get() :

        if event.type == QUIT :
            pygame.quit()
            sys.exit()

    #mise à jour des instruction de déplacement (à chaque itération)

    mycursor.execute("SELECT * FROM position_cible WHERE id_cible=1")
    myresult = mycursor.fetchall()
    mydb.commit()
    position_perso = position_perso.move(myresult[0][1],myresult[0][2])
    font = pygame.font.SysFont(None, 48)
    nom = font.render("Client Clicker", True, "green")
    fond = pygame.Surface((800, 600))
    fond.fill((10, 186, 181))
    fond = fond.convert()

    fenetre.blit(fond, fenetre_rect)
    fenetre.blit(perso, position_perso)
    fenetre.blit(nom, (280, 40))



    pygame.display.flip()