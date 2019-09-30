from PyQt5 import QtWidgets
import pygame
import sys

pygame.init()
fenetre = pygame.display.set_mode((640, 480))
s = pygame.Surface((640, 480))
fond = pygame.image.load("background.jpg").convert()
s.blit(fond, (0, 0))
fenetre.blit(s, (0, 0))
pygame.display.flip()
