import sys
import os
import thread
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
global pygame

class Fen(QWidget):
    def __init__(self):
        super().__init__()
        self.lanceUI()  # Appelle la methode lanceUI ici plus bas

    def lanceUI(self):
        self.resize(500, 300)  # On donne la taille de la fenetre
        self.setWindowTitle("Titre de la fenetre")
        self.show()  # On montre la fenetre

class Panel (QFrame):
    def __init__(self, wTaille):
        global pygame
        QFrame.__init__(self)
        self.resize(500, 300)
        self.show
        os.environ['SDL_WINDOWID'] = str(self.winId())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame
        pygame.display.init()
        window = pygame.display.set_mode(wTaille)
        fond = pygame.image.load("background.jpg").convert()
        window.blit(fond, (0, 0))
        pygame.display.flip()
        

class MyFrame (QWidget):
    def __init__(self, wTaille):
        QWidget.__init__(self)
        self.pnlPanel = Panel(wTaille)
         

monApp = QApplication(sys.argv)  # On defini une nouvelle application
frame = MyFrame((500, 300))






sys.exit(monApp.exec_())
