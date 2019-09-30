# Liste des classes (dans l'ordre) :
# Tile
# TableauCarte
# ViewerCarte
# Fenetre
# MonViewer


import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QCursor, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsItem, QGraphicsScene, QGraphicsView, QGraphicsItemGroup, QGraphicsRectItem
import mss  # Pour la classe Fenetre de test


class GraphVillage(QGraphicsRectItem):
    "Classe servant a representer un village sur la carte"

    def __init__(self, posX, posY, village, parent):
        QGraphicsItem.__init__(self, parent)
        self.x = (posX - posY + 1) * 173 / 2 - 50
        self.y = -(posX + posY) * 150 + 50
        self.village = village
        self.setRect(self.x, self.y, 100, 100)
        self.setBrush(QBrush(QColor('145')))

    def mousePressEvent(self, mouseEvent):
        print("Appui village")

    def boundingRect(self):
        return QtCore.QRectF(self.x, self.y, 100, 100)


class GraphVille(QGraphicsRectItem):
    "Classe servant a representer une ville sur la carte"


class GraphArmee(QGraphicsRectItem):
    "Classe servant a representer une armee sur la carte"


class Tile (QGraphicsItem):
    "Classe permettant de créer une tuile"

    def __init__(self, posX, posY, tuile, parent=None):
        QGraphicsItem.__init__(self, parent)

        self.tuile = tuile
        self.x = posX
        self.y = posY

    def boundingRect(self):
        return QtCore.QRectF(self.x, self.y, 173, 200)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(QtCore.QPointF(self.x, self.y), self.tuile)

    def moveBy(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy


class TableauCarte():
    "Classe servant a creer un tableau depuis un fichier passe en argument"

    def __init__(self, fichier):
        with open(fichier, 'r') as fichier:
            self.structure = []
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
                self.structure.append(ligneNiveau)
                numLigne = numLigne + 1
        self.largeur = 173 * max(len(self.structure[0]), len(self.structure[1]))
        self.hauteur = len(self.structure)


class ViewerCarte(QGraphicsView):
    "Classe creant le viewer qui contient la map"

    def __init__(self, _tableauCarte, _tileSet, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        self.parent = parent
        self.parent.viewer = self
        global x
        global y
        global zoom1
        zoom1 = 1
        x = 0
        y = 0

        self.scene = QGraphicsScene()
        self.groupe = QGraphicsItemGroup(None)
        self.tableauCarte = _tableauCarte.structure

        self.curseur = QCursor()

        # On cree toutes les sprites
        self.tileSet = QPixmap(_tileSet)
        self.foret = self.tileSet.copy(0, 0, 173, 200)
        self.plaine = self.tileSet.copy(173, 0, 173, 200)
        self.champs = self.tileSet.copy(2 * 173, 0, 173, 200)
        self.mer = self.tileSet.copy(3 * 173, 0, 173, 200)
        self.montagnes = self.tileSet.copy(4 * 173, 0, 173, 200)
        self.neige = self.tileSet.copy(5 * 173, 0, 173, 200)
        self.plage = self.tileSet.copy(6 * 173, 0, 173, 200)
        self.creationCarte()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.resize(500, 500)
        self.resize(self.parent.largeur, self.parent.hauteur)
        self.groupe.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.groupe)
        self.addVillage(-2, -6, None)
        self.setScene(self.scene)

    def creationCarte(self):
        "Methode pour creer la carte, cette methode ajoute des tuilles au groupe de tuilles"

        numLigne = 0
        for ligne in self.tableauCarte:
            numCase = 0
            for sprite in ligne:
                if numLigne % 2 == 0:
                    x = numCase * 173
                    y = numLigne * 150  # 200 - 50
                else:
                    x = numCase * 173 + 86
                    y = numLigne * 150
                if sprite == '1':
                    self.groupe.addToGroup(Tile(x, y, self.foret, self.groupe))
                elif sprite == '2':
                    self.groupe.addToGroup(Tile(x, y, self.plaine, self.groupe))
                elif sprite == '3':
                    self.groupe.addToGroup(Tile(x, y, self.champs, self.groupe))
                elif sprite == '4':
                    self.groupe.addToGroup(Tile(x, y, self.mer, self.groupe))
                elif sprite == '5':
                    self.groupe.addToGroup(Tile(x, y, self.montagnes, self.groupe))
                elif sprite == '6':
                    self.groupe.addToGroup(Tile(x, y, self.neige, self.groupe))
                elif sprite == '7':
                    self.groupe.addToGroup(Tile(x, y, self.plage, self.groupe))
                numCase = numCase + 1
            numLigne = numLigne + 1

    # Fonctions pour les zooms a la souris
    def wheelEvent(self, event):
        self.zoom(event.angleDelta().y() / 110.0)

    def zoom(self, facteur):
        if facteur < 0.0:
            facteur = -1.0 / facteur
        self.scale(facteur, facteur)

    # Fonctions pour bouger la carte
    def mouseMoveEventTest(self, event):  # A modifier (empeche le mouvement du groupe)
        global x
        global y
        while self.curseur.pos().x() <= 3:
            print("gauche")
            self.bouger(10, 0)
        while self.curseur.pos().y() <= 3:
            print("haut")
            self.bouger(0, 10)
        while self.curseur.pos().x() >= self.parent.largeur - 3:
            print("gauche")
            self.bouger(-10, 0)
        while self.curseur.pos().y() >= self.parent.hauteur - 3:
            print("bas")
            self.bouger(0, -10)

    def bouger(self, dx, dy):  # Inutile actuellement
        global x
        global y
        global zoom1

        x = x + dx
        y = y + dy
        self.scene.setSceneRect(0, 0, x, y)
        self.scene.update(self.scene.sceneRect())
        self.update()

    # Fonctions pour interragir avec la carte
    def keyPressEvent(self, keyEvent):
        key = keyEvent.key()
        if key == QtCore.Qt.Key_Escape:
            if self.parent.menus is None:
                self.parent.quitter()
            else:
                if self.parent.menus.ui.wMenus.isHidden():
                    self.parent.menus.ui.wMenus.show()
                    self.parent.menus.ui.wMenus.setFocus()
        elif key == QtCore.Qt.Key_A:
            if self.parent.menus is None:
                return None
            self.parent.menus.testVilles()
            self.parent.menus.appuiCentreVille()
        elif key == QtCore.Qt.Key_B:
            self.changer(self.groupe.x() + 0, self.groupe.y() + 0, self.montagnes)
        elif key == QtCore.Qt.Key_C:
            self.changer(self.groupe.x() + 0, self.groupe.y() + 0, self.mer)
        elif key == QtCore.Qt.Key_Z:
            self.zoom(2)
        else:
            print(key)

    def quelCase(self, x, y, tableauCarte):
        print('test')

    def changer(self, x, y, tuile):
        self.groupe.addToGroup(Tile(x, y, tuile))
        self.scene.update()

    def addVillage(self, x, y, village):
        "Mathode pour ajouter un village en position x,y"
        self.scene.addItem(GraphVillage(x, y, village, None))


class Fenetre (QMainWindow):
    "Classe pour la creation d'une fenetre (classe de tests)"

    def __init__(self, parent=None):
        super(Fenetre, self).__init__(parent=parent)
        mon = mss.mss().monitors[1]
        self.app = app
        self.hauteur = mon["height"]
        self.largeur = mon["width"]
        self.menus = None
        self.setWindowTitle("Prototype")

    def quitter(self):
        "Pour quitter vers le bureau"

        sys.exit(self.app.exec_())


class MonViewer(QGraphicsView):
    "Classe de test"

    def __init__(self, parent=None, posX=-1000, posY=-1000, maxX=2000, maxY=2000):
        QGraphicsView.__init__(self, parent=parent)
        self.scene = QGraphicsScene(self)
        self.setGeometry(QtCore.QRect(posX, posX, maxX, maxY))


# Premier affichage de la map avec pyQt5
# C'est ainsi qu'il doit etre appele dans un autre fichier
# Besoin de rien d'autre que lui-meme
if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    tableauCarte = TableauCarte("Prototype2.txt")
    viewer = ViewerCarte(tableauCarte, "tileset V1.png", fenetre)
    viewer.groupe.setFlag(QGraphicsItem.ItemIsMovable)
    fenetre.showFullScreen()
    sys.exit(app.exec_())

# Test
if __name__ == '__main__2':
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    viewer = MonViewer(fenetre)
    pixmap = QPixmap("tileset V1.png")
    viewer.scene.addItem(Tile(0, 0, pixmap))
    viewer.setScene(viewer.scene)
    fenetre.show()
    sys.exit(app.exec_())
