from PyQt5 import QtCore, QtWidgets
from InterfaceVillage import InterfaceVillage
from Eco import Eco
from wVille import wVille
from ClassWidget import LCD


class WidgetAutres(QtWidgets.QWidget):
    "Classe servant a creer des widgets de boutons"

    # si il y a un viewer, cela veut dire qu'a la fermeture du widget, le viewer doit recuperer la main, sion, c'est le parent
    def __init__(self, largeur, hauteur, viewer, parent=None):
        super(WidgetAutres, self).__init__(parent=parent)
        self.parent = parent
        self.viewer = viewer
        self.setGeometry(0, 0, largeur, hauteur)
        self.hide()

    def mousePressEvent(self, event):
        "Methode pour quitter la fenetre si on clique a cote"

        self.hide()
        # Redonne ensuite le focus a qui il faut
        if self.viewer is None:
            self.parent.setFocus()
        else:
            self.viewer.setFocus()

    def keyPressEvent(self, keyEvent):
        "Methode pour les racourcis clavier des interfaces"

        key = keyEvent.key()
        if key == QtCore.Qt.Key_Escape:  # Permet de fermer le menus quand on clique sur esc
            self.hide()
            # Redonne ensuite le focus a qui il faut
            if self.viewer is None:
                self.parent.setFocus()
            else:
                self.viewer.setFocus()
        else:
            print(key)


class Boutons ():
    "Classe principale servant a creer toute la GUI"

    def __init__(self, fenetre, viewer):
        fenetre.setWindowModality(QtCore.Qt.NonModal)

        self.fenetre = fenetre
        hauteur = fenetre.hauteur
        largeur = fenetre.largeur

        # Tous les Widgets qui vont etre utilises
        self.wMenus = WidgetAutres(largeur, hauteur, viewer, fenetre)  # Widget du menu esc
        self.wVilles = wVille(largeur, hauteur, viewer, fenetre)  # Widget pour les villes
        self.wVillage = InterfaceVillage(largeur, hauteur, None, fenetre)

        # Widget pour les menus de droite:
        self.wEco = Eco(largeur, hauteur, viewer, fenetre)

        # Affichages de valeurs de ressources:
        self.lcd = LCD(largeur - 100, hauteur - 150, 100, 50, viewer)  # Argent

        # Tous les boutons cree
        # 1) Tous les boutons visibles h24
        # Boutone Menus esc
        self.bouton1 = QtWidgets.QPushButton(viewer)
        self.bouton1.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.bouton1.setObjectName("Bouton1")

        # Bouton events
        self.bouton2 = QtWidgets.QPushButton(viewer)
        self.bouton2.setGeometry(QtCore.QRect(largeur - 50, hauteur / 2 - 150, 50, 50))
        self.bouton2.setObjectName("Bouton2")

        # Bouton recherches
        self.bouton3 = QtWidgets.QPushButton(viewer)
        self.bouton3.setGeometry(QtCore.QRect(largeur - 50, hauteur / 2 - 100, 50, 50))
        self.bouton3.setObjectName("Bouton4")

        # Bouton diplomatie
        self.bouton4 = QtWidgets.QPushButton(viewer)
        self.bouton4.setGeometry(QtCore.QRect(largeur - 50, hauteur / 2 - 50, 50, 50))
        self.bouton4.setObjectName("Bouton4")

        # Bouton taxes
        self.bouton5 = QtWidgets.QPushButton(viewer)
        self.bouton5.setGeometry(QtCore.QRect(largeur - 50, hauteur / 2, 50, 50))
        self.bouton5.setObjectName("Bouton5")

        # Bouton gouvernement
        self.bouton6 = QtWidgets.QPushButton(viewer)
        self.bouton6.setGeometry(QtCore.QRect(largeur - 50, hauteur / 2 + 50, 50, 50))
        self.bouton6.setObjectName("Bouton6")

        # Bouton armées
        self.bouton7 = QtWidgets.QPushButton(viewer)
        self.bouton7.setGeometry(QtCore.QRect(largeur - 50, hauteur / 2 + 100, 50, 50))
        self.bouton7.setObjectName("Bouton7")

        # Bouton de fin du tour
        self.bouton8 = QtWidgets.QPushButton(viewer)
        self.bouton8.setGeometry(QtCore.QRect(largeur - 100, hauteur - 100, 100, 100))
        self.bouton8.setObjectName("Bouton8")

        # Bouton quetes/conditions de victoire
        self.bouton9 = QtWidgets.QPushButton(viewer)
        self.bouton9.setGeometry(QtCore.QRect(largeur - 150, hauteur - 50, 50, 50))
        self.bouton9.setObjectName("Bouton9")

        self.events = QtWidgets.QPushButton(viewer)
        self.events.setGeometry(QtCore.QRect(largeur - 150, hauteur - 100, 50, 50))
        self.events.setObjectName("Events")

        # 2) Boutons du menus exc :
        # Retour au jeu
        self.bouton10 = QtWidgets.QPushButton(self.wMenus)
        self.bouton10.setGeometry(QtCore.QRect(largeur / 2 - 100, hauteur / 2 - 150, 200, 50))
        self.bouton10.setObjectName("Bouton10")

        # Sauvegarder
        self.bouton11 = QtWidgets.QPushButton(self.wMenus)
        self.bouton11.setGeometry(QtCore.QRect(largeur / 2 - 100, hauteur / 2 - 100, 200, 50))
        self.bouton11.setObjectName("Bouton11")

        # Charger
        self.bouton12 = QtWidgets.QPushButton(self.wMenus)
        self.bouton12.setGeometry(QtCore.QRect(largeur / 2 - 100, hauteur / 2 - 50, 200, 50))
        self.bouton12.setObjectName("Bouton12")

        # Quitter vers le menu principal
        self.bouton13 = QtWidgets.QPushButton(self.wMenus)
        self.bouton13.setGeometry(QtCore.QRect(largeur / 2 - 100, hauteur / 2, 200, 50))
        self.bouton13.setObjectName("Bouton13")

        # Quitter vers le bureau
        self.bouton14 = QtWidgets.QPushButton(self.wMenus)
        self.bouton14.setGeometry(QtCore.QRect(largeur / 2 - 100, hauteur / 2 + 50, 200, 50))
        self.bouton14.setObjectName("Bouton14")

        # 3) Boutons de test :
        # Bouton de test affichant l'interface d'une ville
        self.testVille = QtWidgets.QPushButton(viewer)
        self.testVille.setGeometry(QtCore.QRect(50, 0, 50, 50))
        self.testVille.setObjectName("testVille")

        self.retranslateUi(fenetre)
        QtCore.QMetaObject.connectSlotsByName(fenetre)

    def retranslateUi(self, fenetre):
        "Methode pour afficher du texte sur les boutons"

        _translate = QtCore.QCoreApplication.translate
        self.bouton1.setText(_translate("fenetre", "Menus"))
        self.bouton2.setText(_translate("fenetre", "C"))
        self.bouton3.setText(_translate("fenetre", "R"))
        self.bouton4.setText(_translate("fenetre", "D"))
        self.bouton5.setText(_translate("fenetre", "E"))
        self.bouton6.setText(_translate("fenetre", "G"))
        self.bouton7.setText(_translate("fenetre", "A"))
        self.bouton8.setText(_translate("fenetre", "Fin du tour"))
        self.bouton9.setText(_translate("fenetre", "Q"))
        self.bouton10.setText(_translate("fenetre", "Retour au jeu"))
        self.bouton11.setText(_translate("fenetre", "Sauvegarder"))
        self.bouton12.setText(_translate("fenetre", "Charger"))
        self.bouton13.setText(_translate("fenetre", "Retour au menu principal"))
        self.bouton14.setText(_translate("fenetre", "Retour au bureau"))
        self.events.setText(_translate("fenetre", "E"))
        # Boutons des tests :
        self.testVille.setText(_translate("fenetre", "Test villes"))

    def setVille(self, ville):  # La methode pourrait etre changee pour faire une actualisation moins lourde au cas ou ce serait necessaire
        "Methode pour actualiser les interfaces quand on change de ville"

        self.wVilles.setVille(ville)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    fenetre = QtWidgets.QMainWindow()
    widget = QtWidgets.QWidget(fenetre)
    ui = Boutons(fenetre, widget)
    fenetre.setCentralWidget(widget)
    fenetre.show()
    sys.exit(app.exec_())
