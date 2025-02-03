import random
import pygame
import cv2
import handd as htm
import math




pygame.init()

# Définition d'un événement personnalisé
TEMPS_ECOULE_EVENT = pygame.USEREVENT + 1

# création fenetre 
ecran = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Esquive du futur")
ecran.fill("grey")

#création class fusee
class fu:
    def __init__(fish,a):
        fish.image_fusée = a

mon_rectf = pygame.Rect(250,490,100,100)
fusée = fu(pygame.draw.rect(ecran,"red",mon_rectf))
pygame.display.flip()

#création class planete
class pla:
    def __init__(work,b):
        work.image_planete = b


mon_rectp = pygame.Rect(random.randint(60,540),10,100,100)
mon_rectpb = pygame.Rect(random.randint(60,540),-20,20,20)
planete = pla(pygame.draw.rect(ecran,"black",mon_rectp))
planeteb = pla(pygame.draw.rect(ecran,"black",mon_rectpb))


pygame.display.flip()

#initialisation point et Font
POINTS = 0
FONT = pygame.font.Font(None,24)
FONT1 = pygame.font.Font(None,59)



def initialisation_temps():
    global clock, temps_passe, temps_dernier_evenement, temps_debut
    clock = pygame.time.Clock()
    temps_debut = 0
    temps_debut = pygame.time.get_ticks()  # Temps en millisecondes au démarrage du jeu
    temps_passe = 0
    temps_dernier_evenement = temps_debut
    

def chronometre():
    global temps_passe, temps_en_secondes
    temps_actuel = pygame.time.get_ticks()
    temps_passe = temps_actuel - temps_debut
    temps_en_secondes = temps_passe // 1000

 
def affichage_score_et_temps():
    global temps_en_secondes
    SCORE = FONT.render(f"Score : {str(POINTS)} Points", 1 ,"black")
    TEMPS = FONT.render(f"Temps : {str(temps_en_secondes)} Secondes", True ,"black")
    ecran.blit(TEMPS,(10,10))
    ecran.blit(SCORE,(10,40))

def message_defaite():
    global MESSAGE
    MESSAGE = FONT1.render(f"You Loose --> Score : {str(POINTS)} Points", 1 ,"Red")
    ecran.blit(MESSAGE,(12,270))


def affichage_planete_et_fusee():
    ecran.fill("grey")
    pygame.draw.rect(ecran,"red", mon_rectf)
    pygame.draw.rect(ecran,"black",mon_rectp)
    pygame.draw.rect(ecran,"black",mon_rectpb)


collision_detectee = False
def colisions():
    global collision_detectee
    if mon_rectf.colliderect(mon_rectp):
        collision_detectee = True
    if mon_rectf.colliderect(mon_rectpb):
        collision_detectee = True

    

def generer_evenement_temps():
    pygame.event.post(pygame.event.Event(TEMPS_ECOULE_EVENT))
TEMPS_INTERVALLE = 10
pygame.time.set_timer(TEMPS_ECOULE_EVENT, TEMPS_INTERVALLE)

def reinitialisation():
    global collision_detectee, POINTS
    collision_detectee = False
    POINTS = 0
    mon_rectf.x = 250
    mon_rectp.x = random.randint(60,540)
    mon_rectp.y = -50
    mon_rectpb.y = -20
    initialisation_temps()
    pygame.display.flip()



def Jeux_niveau_debutant():
    global POINTS
    pygame.init()
    arret_jeux = False
    continuer_partie = True
    initialisation_temps()
    wCam, hCam = 640, 480
    hand_detector = htm.handDetector(detectionCon=0.7)
    while continuer_partie:
        cap = cv2.VideoCapture(0)  
        cap.set(4, hCam)
        while arret_jeux == False:
            success, img = cap.read()
            img = hand_detector.findHands(img)
            lmList = hand_detector.findPosition(img, draw=False)
            if len(lmList) != 0:
                x1, y1 = lmList[4][1], lmList[4][2]  # doigt 1 (pouce)
                x2, y2 = lmList[8][1], lmList[8][2]  # doigt 2 (index)
                length = math.hypot(x2 - x1, y2 - y1)  # obtient la longueur entre les doigts
            elif len(lmList) == 0:
                length = -100
            print(length)
            cv2.imshow("Img", img)  # montre la video
            for event in pygame.event.get():
                if length == -100:
                    mon_rectf.x = mon_rectf.x
                elif length >= 50:
                    mon_rectf.x -= 1
                elif -99 < length < 50 :
                    mon_rectf.x += 1
                affichage_planete_et_fusee()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        arret_jeux = True
                if event.type == TEMPS_ECOULE_EVENT:
                    mon_rectp.y += 2  # Déplacer la planète vers le bas
                    if mon_rectp.y > 600:
                        mon_rectp.y = -10
                        mon_rectp.x = random.randint(60,540)
                        mon_rectp.width = random.randint(10,50)
                        mon_rectp.height = mon_rectp.width
                        POINTS += 1
            chronometre()
            affichage_planete_et_fusee()
            affichage_score_et_temps()
            colisions()
            if collision_detectee == True :
                arret_jeux = True
            pygame.display.flip()
            clock.tick(60)

        while arret_jeux : 
            message_defaite()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        reinitialisation()
                        arret_jeux = False
                    if event.key == pygame.K_ESCAPE:
                        continuer_partie = False
                        arret_jeux = False

"""

def Jeux_niveau_intermediaire():
    global POINTS
    pygame.init()
    arret_jeux = False
    continuer_partie = True
    initialisation_temps()
    while continuer_partie:
        while arret_jeux == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        arret_jeux = True
                    if event.key == pygame.K_RIGHT:
                        mon_rectf.x += 8
                    if event.key == pygame.K_LEFT:
                        mon_rectf.x -= 8
                elif event.type == TEMPS_ECOULE_EVENT:
                    mon_rectp.y += 3  # Déplacer la planète vers le bas
                    if mon_rectp.y > 600:
                        mon_rectp.y = 0
                        mon_rectp.x = random.randint(60,540)
                        mon_rectp.width = random.randint(30,70)
                        mon_rectp.height = mon_rectp.width
                        POINTS += 1
            chronometre()
            affichage_planete_et_fusee()
            affichage_score_et_temps()
            colisions()
            if collision_detectee == True :
                arret_jeux = True
            pygame.display.flip()
            clock.tick(60)

        while arret_jeux : 
            message_defaite()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        reinitialisation()
                        arret_jeux = False
                    if event.key == pygame.K_ESCAPE:
                        continuer_partie = False
                        arret_jeux = False


def Jeux_niveau_grands_sage_légendaire():
    global POINTS
    pygame.init()
    arret_jeux = False
    continuer_partie = True
    initialisation_temps()
    while continuer_partie:
        while arret_jeux == False:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        arret_jeux = True
                    if event.key == pygame.K_RIGHT:
                        mon_rectf.x += 5
                    if event.key == pygame.K_LEFT:
                        mon_rectf.x -= 5
                elif event.type == TEMPS_ECOULE_EVENT:
                    mon_rectp.y += 2  # Déplacer la planète vers le bas
                    mon_rectpb.y += 1 
                    if mon_rectp.y > 600:
                        mon_rectp.y = 0
                        mon_rectp.x = random.randint(60,540)
                        mon_rectp.width = random.randint(50,100)
                        mon_rectp.height = mon_rectp.width
                        POINTS += 1      
                    if mon_rectpb.y > 600:
                        mon_rectpb.y = -10
                        mon_rectpb.x = random.randint(60,540)
                        mon_rectpb.width = random.randint(10,30)
                        mon_rectpb.height = mon_rectpb.width
                        POINTS += 1
            chronometre()
            affichage_planete_et_fusee()
            affichage_score_et_temps()
            colisions()
            if collision_detectee == True :
                arret_jeux = True
            pygame.display.flip()
            clock.tick(60)

        while arret_jeux : 
            message_defaite()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        reinitialisation()
                        arret_jeux = False
                    if event.key == pygame.K_ESCAPE:
                        continuer_partie = False
                        arret_jeux = False


    

                """