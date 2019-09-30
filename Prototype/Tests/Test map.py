from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem, QGraphicsItemGroup
import sys


class Tile (QGraphicsItem):
    "Classe permettant de créer une tuile"

    def __init__(self, posX, posY, tuile, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemIgnoresParentOpacity)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)  # le fameux flag pour le rendre "bougeable"

        self.tuile = tuile
        self.x = posX
        self.y = posY

    def boundingRect(self):
        return QRectF(0, 0, 0, 0)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(QPointF(self.x, self.y), self.tuile)


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


app = QApplication(sys.argv)
scene = QGraphicsScene()
groupe = QGraphicsItemGroup()

# On crée les sprite
tileSet = QPixmap("tileset V1.png")
foret = tileSet.copy(0, 0, 173, 200)
plaine = tileSet.copy(173, 0, 173, 200)
champs = tileSet.copy(2 * 173, 0, 173, 200)
mer = tileSet.copy(3 * 173, 0, 173, 200)
montagnes = tileSet.copy(4 * 173, 0, 173, 200)
neige = tileSet.copy(5 * 173, 0, 173, 200)
plage = tileSet.copy(6 * 173, 0, 173, 200)

tableauCarte = TableauCarte("Prototype2.txt")

posX = 0
posY = 0
numLigne = 0
for ligne in tableauCarte.structure:
    numCase = 0
    for sprite in ligne:
        if numLigne % 2 == 0:
            x = numCase * 173
            y = numLigne * 150  # 200 - 50
        else:
            x = numCase * 173 + 86
            y = numLigne * 150
        if sprite == '1':
            groupe.addToGroup(Tile(x - posX, y - posY, foret, groupe))
        elif sprite == '2':
            groupe.addToGroup(Tile(x - posX, y - posY, plaine, groupe))
        elif sprite == '3':
            groupe.addToGroup(Tile(x - posX, y - posY, champs, groupe))
        elif sprite == '4':
            groupe.addToGroup(Tile(x - posX, y - posY, mer, groupe))
        elif sprite == '5':
            groupe.addToGroup(Tile(x - posX, y - posY, montagnes, groupe))
        elif sprite == '6':
            groupe.addToGroup(Tile(x - posX, y - posY, neige, groupe))
        elif sprite == '7':
            groupe.addToGroup(Tile(x - posX, y - posY, plage, groupe))
        numCase = numCase + 1
    numLigne = numLigne


rectGris = QGraphicsRectItem(0., 0., 200., 150.)
rectGris.setBrush(QBrush(Qt.lightGray))
groupe.addToGroup(rectGris)


vue = QGraphicsView(scene)
vue.resize(800, 600)
vue.fitInView(groupe, Qt.KeepAspectRatio)

scene.addItem(groupe)
vue.setRenderHints(QPainter.Antialiasing)

groupe.setFlag(QGraphicsItem.ItemIsMovable)

vue.showFullScreen()
sys.exit(app.exec_())
