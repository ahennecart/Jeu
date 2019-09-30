from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QLabel


class InterfaceVillage(QWidget):
    "Classe pour l'interface des villages"

    def __init__(self, largeur, hauteur, viewer, parent=None):
        super(InterfaceVillage, self).__init__(parent=parent)
        self.largeur = largeur
        self.hauteur = hauteur
        self.viewer = viewer
        self.parent = parent
        self.setGeometry(0, 0, largeur, hauteur)
        self.fond = QFrame(self)

        self.fond.setStyleSheet("QFrame {background-color:white; color:darkblue}")
        self.fond.setGeometry(300, 200, largeur - 600, hauteur - 400)  # a modifier (emplacement meilleur)

        self.niveau = 0

        self.hide()

    def mousePressEvent(self, event):
        "Methode pour quitter la fenetre si on clique a cote"

        if (event.x() > 300 and event.x() < self.largeur - 300 and event.y() > 200 and event.y() < self.hauteur - 200):  # Ne fait rien si on clique dans la zone
            return None
        self.hide()
        # Redonne ensuite le focus au widget de la ville
        self.parent.viewer.setFocus()

    def keyPressEvent(self, event):
        "Methode pour les racourcis clavier de l'interfaces"

        key = event.key()
        if key == QtCore.Qt.Key_Escape:  # Permet de fermer le menus quand on clique sur esc
            self.hide()
            # Redonne ensuite le focus au widget de la ville
            self.parent.viewer.setFocus()
        else:
            print(key)


class PushButtonVillage(QPushButton):
    "Classe reimplemantant les QPushButton pour les boutons liés aux batiments"

    def __init__(self, lcd, parent=None):
        super(PushButtonVillage, self).__init__(parent)
        self.lcd = lcd
        self.parent = parent

        # On lui defini un QFrame indiquant le prix :    /!\ ajouter les effets aussi
        self.info = QFrame(parent)
        self.info.setStyleSheet("QFrame {background-color:white; color:darkblue}")
        largeur = self.parent.parent.largeur - 740 - 100
        hauteur = self.parent.parent.hauteur - 200
        self.info.setGeometry(largeur - 30, 20, largeur, hauteur)
        self.label = [QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info),
                      QLabel(self.info)]
        a = 0
        for i in self.label:
            i.setGeometry(0, 20 * a, largeur, 20)
            a += 2
        self.maj()
        self.info.hide()
        self.clicked.connect(self.construire)

    def construire(self):
        a = self.parent.village.construire()
        if(a is not None):
            self.maj()

    def maj(self):
        "methode pour mettre a jour les informations du label"
        cout = self.widget.ville.cout("CV", self.bat)
        ressources = ["Argent", "Bois", "Pierre", "Fer", "Or", "Charbon", "Marbre", "Acier", "Nourriture", "Betail", "Chevaux"]
        b = 0
        constr = self.widget.ville.quelleListeDeConstr("CV")
        if constr[0] == self.ligne.numBat:
            self.label[0].setText("Il reste %s tours de construction" % (str(int(constr[1] - constr[2]))))
            b = 1
        elif cout is None:
            self.label[0].setText("Le batiment est a son niveau maximal")
            b = 1
        else:
            self.niveau = self.widget.ville.batCV[0]
            nvBat = self.widget.ville.batCV[self.bat]
            self.widget.ville.bdd.execute("""SELECT nvCart FROM Ville WHERE Quartier == "CV" AND Batiment == %s AND Niveau == %s""" % (self.bat, nvBat + 1))
            self.nvRequis = self.widget.ville.bdd.fetchall()[0][0]
            if self.niveau < self.nvRequis:
                self.label[0].setText("Ameliorez le quartier pour débloquer de nouveau niveaux")
                b = 1
            else:
                a = 0
                while a < len(ressources):
                    if cout[a + 3] != 0:
                        self.label[b].setText(ressources[a] + " : " + str(cout[a + 3]))
                        self.label[b].show()
                        b += 1
                    a += 1
        a = 0
        while a < len(self.label):
            if a >= b:
                self.label[a].hide()
            a += 1

    def enterEvent(self, event):
        self.info.show()

    def leaveEvent(self, event):
        self.info.hide()
