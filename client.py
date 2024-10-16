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
id=randint(9999999)

# TODO: Système de détection de clic et écriture des coordonées du clic dans une table [position_clic : id_joueur(INT), x(INT), y(INT)]
# TODO: Terminer le système de parties (côté serveur aussi)
# TODO: Faire une interface complete (qui affiche "partie déjà en cours" quand la table SQL go =1 et qui montre un leaderboard à la fin)
while True : # boucle de jeu
    clock.tick(30)
    temps -= 1
    chrono = temps // 30

    #vérification de l'élément "go" (si go==1 alors la cible va vers des coordonées prédifinies en même temps que celle du serveur afin de synchroniser les éléments)

    mycursor.execute("SELECT * FROM go")
    myresult = mycursor.fetchall()
    mydb.commit()
    go = myresult[0][0]
    print(go)
    if go==1:
        position_perso.topleft = (200,300)
        temps=seconde*30
        go=0
    i-=1

    #Permet de quitter

    for event in pygame.event.get() :

        if event.type == QUIT :
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            mycursor.execute("INSERT INTO position_joueur VALUES (%s, %s, %s)", (id, x, y))
            mydb.commit()

    #mise à jour des instruction de déplacement (à chaque itération)

    mycursor.execute("SELECT * FROM position_cible WHERE id_cible=1")
    myresult = mycursor.fetchall()
    mydb.commit()

    x, y = pygame.mouse.get_pos()

    position_viseur.topleft = x - 50, y - 50
    position_perso = position_perso.move(myresult[0][1],myresult[0][2])

    mycursor.execute("SELECT chrono FROM sync")
    chronoserv = mycursor.fetchall()
    mydb.commit()

    font = pygame.font.SysFont(None, 24)
    chronometre = font.render("Chrono : " + str(chronoserv[0][0]) + " s", True, "blue")

    font = pygame.font.SysFont(None, 48)
    synchro = font.render("Désynchronisé", True, "red")

    font = pygame.font.SysFont(None, 48)
    nom = font.render("Client Clicker", True, "green")
    fond = pygame.Surface((800, 600))
    fond.fill((10, 186, 181))
    fond = fond.convert()
    fenetre.blit(viseur, position_viseur)
    fenetre.blit(fond, fenetre_rect)
    fenetre.blit(perso, position_perso)
    fenetre.blit(nom, (280, 40))
    if chrono == chronoserv:
        fenetre.blit(synchro, (280, 80))
    fenetre.blit(chronometre, (20, 20))



    pygame.display.flip()