from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, QGraphicsItemGroup
import sys


class Rond(QGraphicsEllipseItem):
    def __init__(self, a, b, c, d):
        QGraphicsEllipseItem.__init__(self, a, b, c, d)

    def mousePressEvent(self, event):
        print(event.pos())

class Viewer(QGraphicsView):
    def __init__(self, scene):
        QGraphicsView.__init__(self, scene)

    def mouseReleaseEvent(self, event):
        print(event.pos())

app = QApplication(sys.argv)
scene = QGraphicsScene()
groupe = QGraphicsItemGroup()
rectGris = QGraphicsRectItem(0., 0., 200., 150.)
rectGris.setBrush(QBrush(Qt.lightGray))
groupe.addToGroup(rectGris)
vue = Viewer(scene)
vue.resize(800, 600)
vue.fitInView(rectGris, Qt.KeepAspectRatio)

d = 48  # diametre smiley
ox = 4  # largeur oeil
oy = 6  # hauteur oeil
smiley = Rond(-d / 2, -d / 2, d, d)
smiley.setBrush(QBrush(Qt.yellow))
yeux = [QGraphicsEllipseItem(-ox / 2, -oy / 2, ox, oy, parent=smiley) for _ in range(2)]
yeux[0].setPos(-d / 6, -d / 8)
yeux[1].setPos(d / 6, -d / 8)
brush = QBrush(Qt.black)
for oeil in yeux:
    oeil.setBrush(brush)
smiley.setPos(rectGris.mapToScene(rectGris.rect().center()))
groupe.addToGroup(smiley)

scene.addItem(groupe)
vue.setRenderHints(QPainter.Antialiasing)

groupe.setFlag(QGraphicsItem.ItemIsMovable)

vue.show()
sys.exit(app.exec_())
