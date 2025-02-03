import pygame
import random

# Initialisation de pygame
pygame.init()

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (213, 50, 80)
vert = (0, 255, 0)
bleu = (50, 153, 213)

# Dimensions de la fenêtre
dimensions = largeur, hauteur = 800, 600

# Création de la fenêtre
fenetre = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Snake Game")

# Chargement des textures
texture_snake = pygame.image.load("serpent.jpeg")
texture_snake = pygame.transform.scale(texture_snake, (20, 20))

texture_nourriture = pygame.image.load("pomme.jpeg")
texture_nourriture = pygame.transform.scale(texture_nourriture, (20, 20))

texture_fond = pygame.image.load("image.jpeg")
texture_fond = pygame.transform.scale(texture_fond, dimensions)

# Vitesse du snake
horloge = pygame.time.Clock()
vitesse_snake = 10

# Dimensions du snake
taille_bloc = 20

# Fontes
font_style = pygame.font.Font(None, 25)
score_font = pygame.font.Font(None, 35)

# Affichage du score
def afficher_score(score):
    valeur = score_font.render("Score: " + str(score), True, rouge)
    fenetre.blit(valeur, [10, 10])

# Le snake
def notre_snake(taille_bloc, liste_snake):
    for bloc in liste_snake:
        fenetre.blit(texture_snake, (bloc[0], bloc[1]))

# Message de fin
def message(msg, couleur):
    mesg = font_style.render(msg, True, couleur)
    fenetre.blit(mesg, [largeur / 6, hauteur / 3])

def jeu():
    game_over = False
    game_close = False

    x1 = largeur / 2
    y1 = hauteur / 2

    x1_change = 0
    y1_change = 0

    liste_snake = []
    longueur_snake = 1

    # Position aléatoire de la nourriture
    nourriture_x = round(random.randrange(0, largeur - taille_bloc) / taille_bloc) * taille_bloc
    nourriture_y = round(random.randrange(0, hauteur - taille_bloc) / taille_bloc) * taille_bloc

    while not game_over:

        while game_close:
            fenetre.blit(texture_fond, (0, 0))
            message("Perdu! Appuyez sur Q-Quitter ou C-Continuer", rouge)
            afficher_score(longueur_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        jeu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -taille_bloc
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = taille_bloc
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -taille_bloc
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = taille_bloc
                    x1_change = 0

        if x1 >= largeur or x1 < 0 or y1 >= hauteur or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        fenetre.blit(texture_fond, (0, 0))
        fenetre.blit(texture_nourriture, (nourriture_x, nourriture_y))
        liste_snake.append([x1, y1])
        if len(liste_snake) > longueur_snake:
            del liste_snake[0]

        for bloc in liste_snake[:-1]:
            if bloc == [x1, y1]:
                game_close = True

        notre_snake(taille_bloc, liste_snake)
        afficher_score(longueur_snake - 1)

        pygame.display.update()

        if x1 == nourriture_x and y1 == nourriture_y:
            nourriture_x = round(random.randrange(0, largeur - taille_bloc) / taille_bloc) * taille_bloc
            nourriture_y = round(random.randrange(0, hauteur - taille_bloc) / taille_bloc) * taille_bloc
            longueur_snake += 1

        horloge.tick(vitesse_snake)

    pygame.quit()
    quit()

jeu()
