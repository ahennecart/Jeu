import sys
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class Ui_Mainwindow(object):
    def setupUi(self, MainWindow):
        Mainwindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(500, 300)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Ui_Mainwindow()
    ui.setupUi(Mainwindow)
    os.environ['SDL_WINDOWID'] = str(Mainwindow.winId())
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    import pygame
    pygame.display.init()
    window = pygame.display.set_mode((500, 300))
    fond = pygame.image.load("background.jpg").convert()
    window.blit(fond, (0, 0))
    pygame.display.flip()
    Mainwindow.show()
    sys.exit(app.exec_())
