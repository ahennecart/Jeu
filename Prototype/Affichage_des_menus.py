from Gui import Boutons
import Villes
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
import sys
from mss import mss


class ConnectionBoutons():
    'Classe principale servant a affecter les actions a la GUI'

    def __init__(self, fenetre, viewer):
        self.viewer = viewer
        self.fenetre = fenetre
        self.fenetre.menus = self
        self.ui = Boutons(fenetre, viewer)

        self.ui.bouton1.clicked.connect(self.appuiBouton1)
        self.ui.bouton2.clicked.connect(self.appuiBouton2)
        self.ui.bouton3.clicked.connect(self.appuiBouton3)
        self.ui.bouton4.clicked.connect(self.appuiBouton4)
        self.ui.bouton5.clicked.connect(self.appuiBouton5)
        self.ui.bouton6.clicked.connect(self.appuiBouton6)
        self.ui.bouton7.clicked.connect(self.appuiBouton7)
        self.ui.bouton8.clicked.connect(self.appuiBouton8)
        self.ui.bouton9.clicked.connect(self.appuiBouton9)
        self.ui.events.clicked.connect(self.appuiEvents)
        self.ui.bouton10.clicked.connect(self.appuiBouton10)
        self.ui.bouton11.clicked.connect(self.appuiBouton11)
        self.ui.bouton12.clicked.connect(self.appuiBouton12)
        self.ui.bouton13.clicked.connect(self.appuiBouton13)
        self.ui.bouton14.clicked.connect(self.appuiBouton14)
        # Boutons des tests :
        self.ui.testVille.clicked.connect(self.testVilles)

    def appuiBouton1(self):
        print("Menus esc")
        self.ui.wMenus.show()
        self.ui.wMenus.setFocus()

    def appuiBouton2(self):
        print("Credo")

    def appuiBouton3(self):
        print("Recherches")

    def appuiBouton4(self):
        print("Diplo")

    def appuiBouton5(self):
        self.ui.wEco.show()
        self.viewer.hide()
        self.ui.wEco.setFocus()
        print("Econnomie")

    def appuiBouton6(self):
        print("Gouvernement")

    def appuiBouton7(self):
        print("Armees")

    def appuiBouton8(self):
        "fin du tour"
        self.fenetre.joueurEnCour.finDuTour()

    def appuiBouton9(self):
        print("Quetes")

    def appuiEvents(self):
        print("Events")

    def appuiBouton10(self):
        print("Retour au jeu")
        self.ui.wMenus.hide()

    def appuiBouton11(self):
        print("Sauvegarder")

    def appuiBouton12(self):
        print("Charger")

    def appuiBouton13(self):
        print("Retour menus principal")

    def appuiBouton14(self):
        print("Retour bureau")
        self.fenetre.quitter()

    # methodes des tests:
    def testVilles(self):
        self.ui.setVille(self.fenetre.joueurEnCour.listeVilles[0])
        self.ui.wVilles.show()
        self.ui.wVilles.setFocus()

    # fonctions autres :


class Fenetre (QMainWindow):
    "Classe pour la creation d'une fenetre (classe de tests)"

    def __init__(self, parent=None):
        super(Fenetre, self).__init__(parent=parent)
        mon = mss().monitors[1]
        self.app = app
        self.hauteur = mon["height"]
        self.largeur = mon["width"]
        self.menus = None
        self.setWindowTitle("Prototype")

    def quitter(self):
        "Pour quitter vers le bureau"

        sys.exit(self.app.exec_())

    def passerLeTour(self):
        print("Passage de tour")


# Besoin de Gui, Ville et ListeConstruction pour faire marcher les tests
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    widget = QWidget(fenetre)
    ville = Villes.Ville("Hollange", 1000, [200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000, 200000])
    boutons = ConnectionBoutons(fenetre, widget, ville)
    fenetre.setCentralWidget(widget)
    fenetre.showFullScreen()
    sys.exit(app.exec_())
