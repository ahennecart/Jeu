import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QCursor, QBrush, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsItem, QGraphicsScene, QGraphicsView, QGraphicsItemGroup, QGraphicsRectItem


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

    def mousePressEvent(self, event):
        print(event.pos())


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

    def __init__(self, _tableauCarte, _tileSet, scene, groupe, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        self.parent = parent
        global x
        global y
        global zoom1
        zoom1 = 1
        x = 0
        y = 0

        self.scene = scene
        self.groupe = groupe
        self.tableauCarte = _tableauCarte.structure
        self.posX = 0
        self.posY = 0

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
        self.resize(500, 500)
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    # Methode de creation des scenes dans le viewer
    def creationCarte(self):
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
                    self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, self.foret, self.groupe))
                elif sprite == '2':
                    self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, self.plaine, self.groupe))
                elif sprite == '3':
                    self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, self.champs, self.groupe))
                elif sprite == '4':
                    self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, self.mer, self.groupe))
                elif sprite == '5':
                    self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, self.montagnes, self.groupe))
                elif sprite == '6':
                    self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, self.neige, self.groupe))
                elif sprite == '7':
                    self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, self.plage, self.groupe))
                numCase = numCase + 1
            numLigne = numLigne + 1
        self.scene.addItem(self.groupe)
        self.setScene(self.scene)
        self.setMouseTracking(True)

    # Fonctions pour les zooms
    def wheelEvent(self, event):
        self.zoom(event.angleDelta().y() / 110.0)

    def zoom(self, facteur):
        if facteur < 0.0:
            facteur = -1.0 / facteur
        self.scale(facteur, facteur)

    def bouger(self, dx, dy):
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
            sys.exit(app.exec_())
        elif key == QtCore.Qt.Key_A:
            self.zoom(1.02)
        elif key == QtCore.Qt.Key_Q:
            self.zoom(-1.02)
        elif key == 16777235:
            self.bouger(0, 10)
        elif key == 16777237:
            self.bouger(0, -10)
        elif key == 16777234:
            self.bouger(10, 0)
        elif key == 16777236:
            self.bouger(-10, 0)
        else:
            print(key)

    def quelCase(self, x, y, tableauCarte):
        print('test')

    def changer(self, x, y, tuile):
        self.groupe.addToGroup(Tile(x - self.posX, y - self.posY, tuile))
        self.scene.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tableauCarte = TableauCarte("Monde V1.txt")
    scene = QGraphicsScene()
    groupe = QGraphicsItemGroup()

    tileSet = QPixmap("tileset V1.png")
    montagnes = tileSet.copy(4 * 173, 0, 173, 200)

    groupe.addToGroup(Tile(0, 0, montagnes, groupe))
    groupe.addToGroup(Tile(173, 0, montagnes, groupe))
    groupe.addToGroup(Tile(173 * 2, 0, montagnes, groupe))
    groupe.addToGroup(Tile(173 * 3, 0, montagnes, groupe))
    groupe.addToGroup(Tile(173 * 4, 0, montagnes, groupe))
    groupe.addToGroup(Tile(173 * 5, 0, montagnes, groupe))

    view = ViewerCarte(tableauCarte, "tileset V1.png", scene, groupe)
    view.resize(800, 600)

    view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    view.setRenderHints(QPainter.Antialiasing)

    scene.addItem(groupe)
    groupe.setFlag(QGraphicsItem.ItemIsMovable)
    view.show()
    sys.exit(app.exec_())
