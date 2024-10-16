import random
from random import choice, randint
import mysql.connector
import pygame
import sys
from pygame.locals import *
pygame.init()

fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tutoriel Pygame")
fenetre_rect = fenetre.get_rect()
clock = pygame.time.Clock()


#chargement d'un sprite
perso = pygame.image.load("F:\Pygame\perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso.topleft = (100,200)

viseur = pygame.image.load("F:\Pygame\pointeur.png").convert_alpha()
position_viseur = viseur.get_rect()
position_viseur.topleft = pygame.mouse.get_pos()

#définition des variables
multi=10
a=1
b=1
point=0
clic=0
seconde=30
temps=seconde*30
chrono=temps/30
i=90
frequence=45

while temps>0 : # boucle de jeu

    clock.tick(30)
    temps-=1
    chrono=temps//30
    i-=1
    for event in pygame.event.get() :

        if event.type == QUIT :
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1 :
            x,y = pygame.mouse.get_pos()
            if position_perso.left <= x <= position_perso.left+position_perso.width and y>=position_perso.top and y<=position_perso.top+position_perso.height:
                point+=1
            clic+=1

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Algorithme de déplacement>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if position_perso.left >= 700:
            a = 0 - 1 * multi

        elif position_perso.left <= 100:
            a = 1 * multi

        if position_perso.top >= 500:
            b = 0 - 1 * multi

        elif position_perso.top <= 100:
            b = 1 * multi

        if i <= 0:
            a = random.choice([-1, -1, 0, 1, 1]) * multi

            if a == 0:
                b = random.choice([-2, 2]) * multi

            else:
                b = random.choice([-1, -1, 0, 1, 1]) * multi

                if b == 0:
                    a = random.choice([-2, 2]) * multi

            i = frequence
        else:
            pass
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    x,y = pygame.mouse.get_pos()
    position_viseur.topleft = x-50,y-50
    position_perso = position_perso.move(a,b)

    font = pygame.font.SysFont(None, 24)
    chronometre = font.render("Chrono : "+str(chrono)+" s", True, "blue")

    font = pygame.font.SysFont(None, 24)
    score = font.render("Score : "+str(point), True, "green")

    fond = pygame.Surface((800, 600))
    fond.fill((10, 186, 181))
    fond = fond.convert()

    fenetre.blit(fond, fenetre_rect)
    fenetre.blit(perso, position_perso)
    fenetre.blit(viseur, position_viseur)
    fenetre.blit(chronometre, (20, 20))
    fenetre.blit(score, (600, 20))
    if clic>0:
        font = pygame.font.SysFont(None, 24)
        precision = font.render("Précision : "+str(round((point/clic)*100,2))+"%", True, "green")
        fenetre.blit(precision, (600, 40))

    pygame.display.flip()