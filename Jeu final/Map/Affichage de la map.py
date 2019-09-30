import pygame
from pygame.locals import*


pygame.init()

# Chargement du tileset
tileset = pygame.image.load("tileset V1.png")
foret = tileset.subsurface((0, 0, 173, 200))
plaine = tileset.subsurface((173, 0, 173, 200))
champs = tileset.subsurface((2 * 173, 0, 173, 200))
mer = tileset.subsurface((3 * 173, 0, 173, 200))
montagnes = tileset.subsurface((4 * 173, 0, 173, 200))
neige = tileset.subsurface((5 * 173, 0, 173, 200))
plage = tileset.subsurface((6 * 173, 0, 173, 200))


# generation du tableau de tiles
with open("Prototype2.txt", 'r') as fichier:
    structure = []
    numLigne = 0
    # On parcourt les lignes du fichier
    for ligne in fichier:
        ligneNiveau = []
        # On parcour les sprites des lignes
        numCase = 0
        case = ""
        for sprite in ligne:
            if sprite != '\n' and sprite != ',':
                case = case + sprite
            elif sprite == ',':
                ligneNiveau.append(case)
                case = ""
                numCase = numCase + 1
        structure.append(ligneNiveau)
        numLigne = numLigne + 1


# affichage de la map
fenetre = pygame.display.set_mode((numCase * 173 + 86, numLigne * 150 + 50))
# on parcourt la liste structure
numLigne = 0
for ligne in structure:
    # On parcourt les listes de lignes
    numCase = 0
    for sprite in ligne:
        # On calcule la position et on affiche
        if numLigne % 2 == 0:
            x = numCase * 173
            y = numLigne * 150  # 200 - 50
        else:
            x = numCase * 173 + 86
            y = numLigne * 150
        if sprite == '1':
            fenetre.blit(foret, (x, y))
        elif sprite == '2':
            fenetre.blit(plaine, (x, y))
        elif sprite == '3':
            fenetre.blit(champs, (x, y))
        elif sprite == '4':
            fenetre.blit(mer, (x, y))
        elif sprite == '5':
            fenetre.blit(montagnes, (x, y))
        elif sprite == '6':
            fenetre.blit(neige, (x, y))
        elif sprite == '7':
            fenetre.blit(plage, (x, y))
        numCase = numCase + 1
    numLigne = numLigne + 1
pygame.display.flip()

continuer = 1
while continuer == 1:
    for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
        if event.type == QUIT:  # Si un de ces événements est de type QUIT
            continuer = 0  # On arrête la boucle
