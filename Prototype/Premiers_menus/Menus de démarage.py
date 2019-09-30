#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import gui  # import du fichier gui.py généré par pyuic5


class MyWindow(QtWidgets.QMainWindow):

    global choix
    choix = 1

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)

        # définition des fonctions assossiées au boutons
        self.ui.pushButton.clicked.connect(self.ouvreNouvelleCampagne)
        self.ui.pushButton_2.clicked.connect(self.quitterLeJeu)
        self.ui.pushButton_3.clicked.connect(self.ouvreChargerCampagne)
        self.ui.pushButton_4.clicked.connect(self.ouvreOptions)
        self.ui.pushButton_5.clicked.connect(self.ouvreNouvelleCampagne2)
        self.ui.pushButton_6.clicked.connect(self.lancerLaNouvelleCampagne)
        self.ui.pushButton_7.clicked.connect(self.chargerLaCampagne)
        self.ui.pushButton_8.clicked.connect(self.retourMenu1)
        self.ui.radioButton.clicked.connect(self.appuiTremor)
        self.ui.radioButton_2.clicked.connect(self.appuiMisselia)
        self.ui.radioButton_3.clicked.connect(self.appuiDerthor)
        self.ui.radioButton_4.clicked.connect(self.appuiKerouan)
        self.ui.radioButton_5.clicked.connect(self.appuiKraven)

    def ouvreNouvelleCampagne(self):
        print("ouvreNouvelleCampagne")
        self.ui.widget_2.hide()
        self.ui.widget.show()

    def quitterLeJeu(self):
        print("quitterLeJeu")

    def ouvreChargerCampagne(self):
        print("ouvreChargerCampagne")
        self.ui.widget_2.hide()

    def ouvreOptions(self):
        print("ouvreOptions")
        self.ui.widget_2.hide()

    def ouvreNouvelleCampagne2(self):
        print("ouvreNouvelleCampagne2")
        self.ui.widget.hide()
        global choix
        print("Le choix est : " + str(choix))

    def lancerLaNouvelleCampagne(self):
        print("lancerLaNouvelleCampagne")

    def chargerLaCampagne(self):
        print("chargerLaCampagne")

    def retourMenu1(self):
        print("retourMenu1")
        self.ui.widget_2.show()
        self.ui.widget.hide()

    def appuiTremor(self):
        print("appuiTremor")
        global choix
        choix = 1

    def appuiMisselia(self):
        print("appuiMisselia")
        global choix
        choix = 2

    def appuiDerthor(self):
        print("appuiDerthor")
        global choix
        choix = 3

    def appuiKerouan(self):
        print("appuiKerouan")
        global choix
        choix = 4

    def appuiKraven(self):
        print("appuiKraven")
        global choix
        choix = 5


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
