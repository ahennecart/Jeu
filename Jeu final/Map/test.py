from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPainter, QImage, QPixmap
from PyQt5.QtCore import QSize

painter = QPainter()
a = QImage("tileset V1.png")
tile = QPixmap(QSize(a.width(), a.height()))
painter2.setBrush(QBrush(QColor(0, 0, 0, 0)))
painter2.fillRect(0, 0, tile.width(), tile.height())
painter2 = QPainter(tile)
painter2.drawImage(QPoint(0, 0), a)
painter.setBrush(tile.toImage())
