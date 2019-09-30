#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.scene = MyGraphicsScene()
        self.scene.setSceneRect(-500.0, -500.0, 1000.0, 1000.0)
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.setRenderHints(QPainter.Antialiasing)
        self.setCentralWidget(self.view)


    def changeMode(self, mode):  # le flag RubberBand pose problème en mode création
        if mode == 1:
            self.view.setDragMode(QGraphicsView.NoDrag)
        else:
            self.view.setDragMode(QGraphicsView.RubberBandDrag)


class MyGraphicsScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.createMode = 0  # 0 = édition, 1 = création
        self.createState = False  # état de la création utile pour l'évènement mouseMoveEvent
        self.defaultItem = 0  # type d'item à créer
        self.pen = QPen(Qt.black, 2)  # crayon normal d'une figure
        self.penTemp = QPen(Qt.red, 2)  # crayon temporaire à la création
        self.penOver = QPen(Qt.blue, 2)  # crayon quand survolé

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.createMode == 1:  # si click gauche en mode création
            self.firstPoint = e.scenePos()  # on prend le premier point en membre de classe
            self.currentItem = self.createItem()  # on crée l'item sans taille
            self.currentItem.setPen(self.penTemp)  # on fixe sa couleur
            self.addItem(self.currentItem)  # on l'ajoute à la scène
            self.createState = True  # on met l'état création en cours à true
        else:
            QGraphicsScene.mousePressEvent(self, e)  # on fait suivre l'event

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.createState:  # si release gauche en mode création
            if e.scenePos() == self.firstPoint:  # si le point relaché est le même que le premier point
                self.removeItem(self.currentItem)  # on supprime l'item de la scène
                del self.currentItem  # on le supprime même de la mémoire
            else:
                self.currentItem.setPen(self.pen)  # on lui donne sa couleur normale
            self.createState = False
        else:
            QGraphicsScene.mouseReleaseEvent(self, e)  # on fait suivre l'event

    def mouseMoveEvent(self, e):
        if self.createState:  # si on est en cours de création
            self.currentItem.resize(self.firstPoint, e.scenePos())  # on redimentionne
        else:
            QGraphicsScene.mouseMoveEvent(self, e)  # on fait suivre l'event

    def keyPressEvent(self, e):
        key = e.key()
        if(key == Qt.Key_Delete):  # touche suppr
            self.removeSelection()  # on efface la sélection
        elif(key == Qt.Key_Space and not e.isAutoRepeat()):  # touche espace enfoncée
            self.swapToCreateMode()  # on passe en mode création
        elif(key == Qt.Key_Return):
            self.changeDefaultItem()  # on change le type d'item à dessiner

    def keyReleaseEvent(self, e):
        key = e.key()
        if(key == Qt.Key_Space and not e.isAutoRepeat()):  # touche espace relachée
            self.swapToEditMode()  # on revient en mode edit

    def removeSelection(self):  # appelé quand on appuie sur la touche suppr
        items = self.selectedItems()  # on récupère les items sélectionés
        map(self.removeItem, items)  # on les vire de la scène
        for i in items:  # on les détruit totalement
            del i

    def swapToCreateMode(self):
        print("Mode creation")
        self.createMode = 1  # passe en mode création
        self.emit(SIGNAL("modeChanged"), self.createMode)  # emet un signal pour que les items changent de flags

    def swapToEditMode(self):
        print("Mode edition")
        self.createMode = 0  # passe en mode édition
        self.emit(SIGNAL("modeChanged"), self.createMode)  # emet un signal pour que les items changent de flags

    def changeDefaultItem(self):  # change l'item à creer par défaut
        self.defaultItem = (self.defaultItem + 1) % 3  # on l'incrémente de 1
        if self.defaultItem == 0:
            print("lignes")
        elif self.defaultItem == 1:
            print("rectangles")
        elif self.defaultItem == 2:
            print("Ellipses")

    def createItem(self):  # crée l'item voulu
        if self.defaultItem == 0:
            return MyLineItem(self)
        elif self.defaultItem == 1:
            return MyRectItem(self)
        elif self.defaultItem == 2:
            return MyEllipseItem(self)


class VirtualItem(object):
    def __init__(self):
        self.setAcceptHoverEvents(False)  # flag pour est sensible au survol du curseur
        self.setFlag(QGraphicsItem.ItemIsMovable, False)  # le fameux flag pour le rendre "bougeable"
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)  # flag pour le rendre sélectionnable

        self.Q = QObject()  # comme pyQT ne supporte pas l'héritage multiple, seul moyen pour émettre ou recevoir des signaux dans un item
        self.Q.connect(self.parent, SIGNAL("modeChanged"), self.changeMode)  # quand la vue change de mode

    def hoverEnterEvent(self, e):
        print("Enter", self)
        self.setPen(self.parent.penOver)  # couleur de survol

    def hoverLeaveEvent(self, e):
        print("Leave", self)
        self.setPen(self.parent.pen)  # revient à le couleur normale

    def mousePressEvent(self, e):
        print("Item", self, "pressed at ", self.pos())
        QGraphicsItem.mousePressEvent(self, e)  # on fait suivre l'event

    def mouseReleaseEvent(self, e):
        print("Item", self, "released at", self.pos())
        QGraphicsItem.mouseReleaseEvent(self, e)  # on fait suivre l'event

    def changeMode(self, mode):  # change les flags de l'item suivant le mode création ou édition
        if mode == 1:
            self.setAcceptHoverEvents(False)
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        else:
            self.setAcceptHoverEvents(True)
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.setFlag(QGraphicsItem.ItemIsSelectable, True)


class MyLineItem(QGraphicsLineItem, VirtualItem):
    def __init__(self, parent=None):
        QGraphicsLineItem.__init__(self)
        self.parent = parent  # une ref sur le parent est utile plus tard (attacher les signaux)
        VirtualItem.__init__(self)

    def resize(self, p1, p2):  # Méthode pour redimensionner l'item
        self.setLine(QLineF(p1, p2))


class MyRectItem(QGraphicsRectItem, VirtualItem):
    def __init__(self, parent=None):
        QGraphicsRectItem.__init__(self)
        self.parent = parent  # une ref sur le parent est utile plus tard (attacher les signaux)
        VirtualItem.__init__(self)

    def resize(self, p1, p2):  # Méthode pour redimensionner l'item
        self.setRect(QRectF(p1, p2))


class MyEllipseItem(QGraphicsEllipseItem, VirtualItem):
    def __init__(self, parent=None):
        QGraphicsEllipseItem.__init__(self)
        self.parent = parent  # une ref sur le parent est utile plus tard (attacher les signaux)
        VirtualItem.__init__(self)

    def resize(self, p1, p2):  # Méthode poor redimensionner l'item
        self.setRect(QRectF(p1, p2))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
