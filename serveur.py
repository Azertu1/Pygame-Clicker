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

# TODO: Système de lecture des coordonées des clic depuis une table [position_clic : id_joueur(INT), x(INT), y(INT)], verification et ajout de points dans une table [score : id_joueur(INT), score(INT)]
# TODO: Ajout d'un système anticheat (anti spam clic, anti modification BDD score par joueur, vérification des coordonées clic (si les coordonées relatives du clic par rapport à la cible sont toujours les même)
# TODO: Terminer le système de parties (côté client aussi)
while True : # boucle de jeu

    clock.tick(30)
    i-=1
    temps-=1
    mycursor.execute(str("UPDATE sync SET chrono ="temps))
    mydb.commit()

    #La pause toute les x secondes permet de synchroniser les position de tout les client connectés en reglant l'élément "go" du tableau SQL à 1. Cela déplace instantanément les cibles à des coordonées prédéfinies (identique dans les clients et le serveur)

    if pause:
        pause=False
        print("unpause")
        mycursor.execute(str("UPDATE go SET go = 0  WHERE go = 1"))

    if temps<=0:
        mycursor.execute(str("UPDATE go SET go = 1  WHERE go = 0"))
        mydb.commit()
        temps=seconde*30
        position_perso.topleft = (200,300)
        pause=True
        print("pause")

    #Permet de quitter le programme

    for event in pygame.event.get() :

        if event.type == QUIT :
            pygame.quit()
            sys.exit()

    #Mise à jour des instruction de déplacement dans le tableau SQL (une fois toute les 45 itérations)

    if position_perso.left>=700:
        a=0-1*multi
        mycursor.execute(str("UPDATE position_cible SET x = "+str(a)+" WHERE id_cible = 1"))
        mydb.commit()


    elif position_perso.left<=100:
        a=1*multi
        mycursor.execute(str("UPDATE position_cible SET x = "+str(a)+" WHERE id_cible = 1"))
        mydb.commit()


    if position_perso.top>=500:
        b=0-1*multi
        mycursor.execute(str("UPDATE position_cible SET y = "+str(b)+" WHERE id_cible = 1"))
        mydb.commit()


    elif position_perso.top<=100:
        b=1*multi
        mycursor.execute(str("UPDATE position_cible SET y = "+str(b)+" WHERE id_cible = 1"))
        mydb.commit()


    elif not(pause):
        if i<=0:
            a=randint(-1,1)*multi
            b=randint(-1,1)*multi
            mycursor.execute(str("UPDATE position_cible SET x = "+str(a)+" WHERE id_cible = 1"))
            mydb.commit()
            mycursor.execute(str("UPDATE position_cible SET y = "+str(b)+" WHERE id_cible = 1"))
            mydb.commit()
            i=frequence
        else:
            pass

    #instruction de déplacement nulle pendant la pose (les cibles reste fixe pendant une itération)

    elif pause:
            a=0
            b=0
            mycursor.execute(str("UPDATE position_cible SET x = "+str(a)+" WHERE id_cible = 1"))
            mydb.commit()
            mycursor.execute(str("UPDATE position_cible SET y = "+str(b)+" WHERE id_cible = 1"))
            mydb.commit()


    position_perso = position_perso.move(a,b)

    font = pygame.font.SysFont(None, 48)
    nom = font.render("Serveur Clicker", True, "green")
    fond = pygame.Surface((800, 600))
    fond.fill((10, 186, 181))
    fond = fond.convert()

    fenetre.blit(fond, fenetre_rect)
    fenetre.blit(perso, position_perso)
    fenetre.blit(nom, (270, 40))



    pygame.display.flip()