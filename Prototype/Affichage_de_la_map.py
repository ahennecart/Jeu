# Liste des classes (dans l'ordre) :
# Tile
# GraphVillage
# GraphVille
# GraphArmee
# Scene
# TableauCarte
# TableauRessources
# ViewerCarte
# Fenetre


# /!\ 2 systemes de coordonnees, cubique (x, y, z) pour le programme et pixel (x, y) pour l'affichange


import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QCursor, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsItem, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsProxyWidget, QPushButton
import mss  # Pour la classe Fenetre de test


class Tile (QGraphicsItem):
    "Classe permettant de créer une tuile"

    def __init__(self, posX, posY, tuile, viewer):
        QGraphicsItem.__init__(self)

        self.tuile = tuile
        self.x = (posX - posY + 1) * 173 / 2 - 50  # Coordonnees cubique a coordonnees pixel
        self.y = -(posX + posY) * 150 + 50
        self.posX = posX  # Coordonnees cubique (z = -(x + y))
        self.posY = posY
        self.viewer = viewer
        self.ressource = []  # Tableau reprennant toutes les ressources presentes sur la case (1 : fer; 2 : or; 3 : marbre; 4 : charbon; 5 : betail sauvage; 6 : chevaux sauvages; 7 : bois; 8 : pieree)

    def boundingRect(self):
        return QtCore.QRectF(self.x, self.y, 173, 200)

    def paint(self, painter, option, widget=None):
        self.painter = painter
        if(self.tuile is None):
            return None
        painter.drawPixmap(QtCore.QPointF(self.x, self.y), self.tuile)

    def moveBy(self, dx, dy):
        self.x = self.x + dx  # Coordonnees pixel
        self.y = self.y + dy

    # Fonction pour recuperer un clic
    def mousePressEvent(self, event):
        print("clic en ", (self.posX, self.posY))
        typeTuile = self.viewer.quelTuile(self.tuile)
        print("Le type est : " + str(typeTuile))
        print("Les ressources sont : " + str(self.ressource))
        return None


class GraphVillage(Tile):
    "Classe servant a representer un village sur la carte avec un QGraphicsItem"

    def __init__(self, posX, posY, village, tuile, fenetre):
        self.x = posX
        self.y = posY
        Tile.__init__(self, self.x, self.y, tuile, fenetre.viewer)
        self.village = village
        self.fenetre = fenetre

    def mousePressEvent(self, mouseEvent):
        print("Appui village")
        if(self.fenetre.joueurEnCour != self.village.ville.joueur):
            self.village.changerVille(self.fenetre.joueurEnCour.listeVilles[0])
            return None
        self.village.clic()


class GraphVille(Tile):
    "Classe servant a representer une ville sur la carte"

    def __init__(self, posX, posY, ville, tuile, fenetre):
        self.x = posX
        self.y = posY
        Tile.__init__(self, self.x, self.y, tuile, fenetre.viewer)
        self.ville = ville
        self.fenetre = fenetre

    def mousePressEvent(self, mouseEvent):
        print("Appui ville")
        if(self.fenetre.joueurEnCour != self.ville.joueur):
            return None
        self.ville.clic()


class GraphArmee(QGraphicsRectItem):
    "Classe servant a representer une armee sur la carte"

    def __init__(self, posX, posY, armee, parent):
        QGraphicsItem.__init__(self, parent)
        self.x = (posX - posY + 1) * 173 / 2 - 50
        self.y = -(posX + posY) * 150 + 50
        self.armee = armee
        self.setRect(self.x, self.y, 100, 100)
        self.setBrush(QBrush(QColor(255, 255, 255)))

    def mousePressEvent(self, mouseEvent):
        print("Appui armee")

    def boundingRect(self):
        return QtCore.QRectF(self.x, self.y, 100, 100)


class Scene(QGraphicsScene):
    "Classe servant a creer une scene"

    def __init__(self):
        QGraphicsScene.__init__(self)
        self.x = 0
        self.y = 0
        self.posX = 0
        self.posY = 0
        self.a = 1

    def mouseMoveEvent(self, event):
        if(event.buttons() & QtCore.Qt.LeftButton and self.a == 1):
            self.a = 0
            self.posX = event.scenePos().x()
            self.posY = event.scenePos().y()
            self.a = 2
        elif(event.buttons() & QtCore.Qt.LeftButton and self.a == 2):
            self.a = 0
            self.x = self.x + (self.posX - event.scenePos().x()) * 2
            self.y = self.y + (self.posY - event.scenePos().y()) * 2
            self.setSceneRect(self.x, self.y, 1, 1)
            self.a = 1
        else:
            self.a = 1
        return None


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
        self.largeur = max(len(self.structure[0]), len(self.structure[1]))
        self.hauteur = len(self.structure)


class TableauRessources():
    "Classe servant a creer un tableau de ressource depuis un fichier passe en argument"

    def __init__(self, fichier, nbLigne):
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
                if numLigne >= nbLigne:
                    break
        self.largeur = max(len(self.structure[0]), len(self.structure[1]))
        self.hauteur = len(self.structure)


class ViewerCarte(QGraphicsView):
    "Classe creant le viewer qui contient la map"

    def __init__(self, _tableauCarte, _tableauRessource, _tileSet, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        self.parent = parent
        self.parent.viewer = self
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        global x
        global y
        global zoom1
        zoom1 = 1
        x = 0
        y = 0

        self.scene = Scene()
        self.tableauCarte = _tableauCarte.structure
        self.tableauRessource = _tableauRessource.structure

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
        self.ville = self.tileSet.copy(6 * 173, 200, 173, 200)
        self.village = self.tileSet.copy(6 * 173, 2 * 200, 173, 200)
        self.creationCarte()
        self.creationRessources()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.resize(self.parent.largeur, self.parent.hauteur)
        self.setScene(self.scene)

        # Sans les lignes ici, le deplacement de la carte bug, va savoir pourquoi :/ ...   (autant en faire en estrer egg lol)
        self.proxy = QGraphicsProxyWidget()
        self.bouton = QPushButton("Ester Egg")
        self.bouton.setGeometry(-10000, -10000, 200, 200)
        self.proxy.setWidget(self.bouton)
        self.scene.addItem(self.proxy)
        # Fin des lignes contre le bug intenpestif

        self.scene.setSceneRect(0, 0, 1, 1)

    def creationCarte(self):
        "Methode pour creer la carte, cette methode ajoute des tuilles a la scene"

        self.tableauTiles = self.tableauCarte
        z = 0  # = numero de la ligne (0 en haut)
        x, y = 0, 0
        for ligne in self.tableauCarte:
            numColone = 0
            if(z % 2 == 0):
                x = -z / 2
                y = -z / 2
            else:
                x = -z // 2 + 1
                y = -z // 2
            for sprite in ligne:
                if sprite == '1':
                    self.tableauTiles[z][numColone] = Tile(x, y, self.foret, self)
                    self.tableauTiles[z][numColone].ressource.append(7)
                elif sprite == '2':
                    self.tableauTiles[z][numColone] = Tile(x, y, self.plaine, self)
                    self.tableauTiles[z][numColone].ressource.append(8)
                elif sprite == '3':
                    self.tableauTiles[z][numColone] = Tile(x, y, self.champs, self)
                elif sprite == '4':
                    self.tableauTiles[z][numColone] = Tile(x, y, self.mer, self)
                elif sprite == '5':
                    self.tableauTiles[z][numColone] = Tile(x, y, self.montagnes, self)
                    self.tableauTiles[z][numColone].ressource.append(8)
                elif sprite == '6':
                    self.tableauTiles[z][numColone] = Tile(x, y, self.neige, self)
                elif sprite == '7':
                    self.tableauTiles[z][numColone] = Tile(x, y, self.plage, self)
                self.scene.addItem(self.tableauTiles[z][numColone])
                numColone += 1
                x += 1
                y -= 1
            z += 1

    def creationRessources(self):
        "Methode pour donner des ressources aux tuiles"

        a = 0
        for ligne in self.tableauRessource:
            b = 0
            for ress in ligne:
                if ress == '1':
                    self.tableauTiles[a][b].ressource.append(1)
                elif ress == '2':
                    self.tableauTiles[a][b].ressource.append(2)
                elif ress == '3':
                    self.tableauTiles[a][b].ressource.append(3)
                elif ress == '4':
                    self.tableauTiles[a][b].ressource.append(4)
                elif ress == '5':
                    self.tableauTiles[a][b].ressource.append(5)
                elif ress == '6':
                    self.tableauTiles[a][b].ressource.append(6)
                b += 1
            a += 1

    # Fonctions pour les zooms a la souris
    def wheelEvent(self, event):
        self.zoom(event.angleDelta().y() / 110.0)

    def zoom(self, facteur):
        if facteur < 0.0:
            facteur = -1.0 / facteur
        self.scale(facteur, facteur)

    # Fonctions pour interragir avec la carte
    def keyPressEvent(self, keyEvent):
        key = keyEvent.key()
        if key == QtCore.Qt.Key_Escape:
            if self.parent.menus is None:
                self.parent.quitter()
            else:
                if self.parent.boutons.ui.wMenus.isHidden():
                    self.parent.boutons.ui.wMenus.show()
                    self.parent.boutons.ui.wMenus.setFocus()
        elif key == QtCore.Qt.Key_A:
            if self.parent.menus is None:
                return None
            self.parent.boutons.testVilles()
            self.parent.boutons.ui.wVilles.afficheCV()
        elif key == QtCore.Qt.Key_B:
            self.changer(0, 0, self.montagnes)
        elif key == QtCore.Qt.Key_C:
            self.changer(0, 0, self.mer)
        elif key == QtCore.Qt.Key_Z:
            self.zoom(2)
        else:
            print(key)

    def quelTuile(self, tuile):
        "Methode pour savoir quel est le type de tuile"
        if(tuile == self.foret):
            return 1
        elif(tuile == self.plaine):
            return 2
        elif(tuile == self.champs):
            return 3
        elif(tuile == self.mer):
            return 4
        elif(tuile == self.montagnes):
            return 5
        elif(tuile == self.neige):
            return 6
        elif(tuile == self.plage):
            return 7
        return -1

    def changer(self, x, y, tuile):  # a modifier pour que ca marche autre part qu'en (0, 0)
        "Methode pour changer la case du tile"
        self.scene.removeItem(self.tableauTiles[x][y])
        self.tableauTiles[x][y] = Tile(x, y, tuile, self)
        self.scene.addItem(self.tableauTiles[x][y])
        self.scene.update()

    def addVillage(self, x, y, village):
        "Methode pour ajouter un village en position x,y"
        self.scene.addItem(GraphVillage(x, y, village, self.village, self.parent))
        # self.scene.addItem(GraphArmee(x + 1, y + 2, None, None))

    def addVille(self, ville):
        "Methode pour ajouter une ville en position x, y"
        self.scene.addItem(GraphVille(ville.x, ville.y, ville, self.ville, self.parent))


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


# Premier affichage de la map avec pyQt5
# C'est ainsi qu'il doit etre appele dans un autre fichier
# Besoin de rien d'autre que lui-meme
if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    tableauCarte = TableauCarte("Prototype2.txt")
    viewer = ViewerCarte(tableauCarte, "tileset V1.png", fenetre)
    fenetre.showFullScreen()
    sys.exit(app.exec_())
