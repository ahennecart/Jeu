import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsItem, QGraphicsScene, QGraphicsView


class Tile (QGraphicsItem):
    "Classe permettant de créer une tuile"

    def __init__(self, posX, posY, tuile):
        QGraphicsItem.__init__(self)

        self.tuile = tuile
        self.x = posX
        self.y = posY

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 0, 0)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(QtCore.QPointF(self.x, self.y), self.tuile)


class Fenetre (QMainWindow):

    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer
        self.setupUI()

    def setupUI(self):
        self.setObjectName("MainWindow")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.resize(500, 500)
        self.setUnifiedTitleAndToolBarOnMac(False)
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.widget = self.viewer
        self.widget.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.widget.setObjectName("viewer")
        self.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(self)
        self.mainToolBar.setObjectName("mainToolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")


# Affichage de la map
app = QApplication(sys.argv)

viewer = QGraphicsView()
scene = QGraphicsScene()

# On cree toutes les tuiles
tileSet = QPixmap("tileset V1.png")
foret = tileSet.copy(0, 0, 173, 200)
plaine = tileSet.copy(173, 0, 173, 200)
champs = tileSet.copy(2 * 173, 0, 173, 200)
mer = tileSet.copy(3 * 173, 0, 173, 200)
montagnes = tileSet.copy(4 * 173, 0, 173, 200)
neige = tileSet.copy(5 * 173, 0, 173, 200)
plage = tileSet.copy(6 * 173, 0, 173, 200)

# On ajoute les tuiles a la scene
scene.addItem(Tile(0, 0, foret))
scene.addItem(Tile(173, 0, plaine))

# On cree un viewer contenant la scene
viewer.setScene(scene)

# On cree une fenetre
fenetre = Fenetre(viewer)
fenetre.show()
sys.exit(app.exec_())
