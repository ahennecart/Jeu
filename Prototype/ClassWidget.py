from math import log10
from PyQt5.QtWidgets import QWidget, QLCDNumber, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt


class LCD(QLCDNumber):
    "Classe reimplemantant les QLCDNumber pour en adapter l'usage"

    def __init__(self, posX, posY, x, y, parent=None):
        super(LCD, self).__init__(parent)
        self.parent = parent
        self.posX = posX
        self.posY = posY
        self.setGeometry(posX, posY, x, y)

    def display(self, valeur):
        "Methode pour afficher la valeur du LCD et regler sa taille"

        if valeur <= 0:
            self.setDigitCount(1)
            super(LCD, self).display(0)
            return None
        if self.digitCount() != int(log10(valeur) + 1):
            self.setDigitCount(int(log10(valeur) + 1))
        super(LCD, self).display(valeur)


class Cartier(QWidget):
    "Classe pour representer un cartier de la ville avec les batiments a construire"

    def __init__(self, largeur, hauteur, listeNom, quartier, parent=None):
        super(Cartier, self).__init__(parent=parent)
        self.parent = parent
        self.setGeometry(100, 150, largeur, hauteur - 100)
        self.fond = QFrame(self)

        # hauteur et largeur de l'ecran, ne pas confondre avec hauteur et largeur du parent
        self.hauteur = hauteur - 100
        self.largeur = largeur
        self.quartier = quartier
        self.fond.setStyleSheet("QFrame {background-color:white}")
        self.fond.setGeometry(0, 0, self.largeur, self.hauteur)
        self.ville = self.parent.parent.joueurEnCour.listeVilles[0]

        # On cree les batiments :
        self.listeBat = []
        for i in range(0, len(listeNom)):
            self.listeBat.append(LigneBat(listeNom[i], i, self.quartier, self))

        self.hide()

    def majBat(self):
        "Methode pour mettre a jour l'onglet des batiments (cacher et montrer ceux qui peuvent etre construit ou non)"

        quart = self.ville.quelQuartier(self.quartier)
        nvQuart = quart[0]
        for i in range(1, len(quart)):
            self.ville.bdd.execute("""SELECT nvQuart FROM Ville WHERE Quartier == "%s" AND Batiment == %s AND Niveau == 1""" % (self.quartier, i))
            nv = self.ville.bdd.fetchall()[0][0]
            if nvQuart < nv:
                self.listeBat[i].hide()
            else:
                self.listeBat[i].show()

    def setVille(self, ville):
        "Methode permettant de mettre a jour en fonction de la ville"
        self.ville = ville
        for i in self.listeBat:
            i.maj()
        self.majBat()

    def mousePressEvent(self, event):
        "Methode pour annuler le mouse press du wville"

    def keyPressEvent(self, event):
        "Methode pour les racourcis clavier de l'interfaces"

        key = event.key()
        if key == Qt.Key_Escape:  # Permet de fermer le menus quand on clique sur esc
            self.hide()
            # Redonne ensuite le focus au viewer
            self.parent.hide()
            self.parent.viewer.setFocus()
        else:
            print(key)


class LigneBat(QWidget):
    "Classe pour une ligne dans les widget bat"

    def __init__(self, nom, numBat, quartier, parent=None):
        super(LigneBat, self).__init__(parent=parent)
        self.setGeometry(20, 20 * (numBat + 1) + 50 * numBat, (parent.parent.parent.largeur - 100) / 2, 50)
        self.nom = nom
        self.numBat = numBat
        self.quartier = quartier

        self.batQuart = parent.ville.quelQuartier(self.quartier)

        self.parent = parent
        self.labBat = QLabel(self)
        self.labBat.setText(nom)
        self.labBat.setGeometry(0, 0, 400, 50)
        self.LCDNvBat = QLCDNumber(self)
        self.LCDNvBat.setDigitCount(2)
        self.LCDNvBat.setGeometry(400, 0, 50, 50)
        self.boutBat = PushButtonBat(numBat, self.LCDNvBat, self, self.quartier, parent)
        self.boutBat.setText("Upgrade")
        self.boutBat.setGeometry(20 + 400 + 50, 0, (parent.largeur) / 2 - 40 - 400 - 100, 50)
        if numBat != 0:
            self.hide()

    def maj(self):
        self.batQuart = self.parent.ville.quelQuartier(self.quartier)
        self.LCDNvBat.display(self.batQuart[self.numBat])
        self.boutBat.maj()


class PushButtonBat(QPushButton):
    "Classe reimplemantant les QPushButton pour les boutons liés aux batiments"

    def __init__(self, numBat, lcd, ligne, quartier, parent=None):
        super(PushButtonBat, self).__init__(ligne)
        self.numBat = numBat
        self.lcd = lcd
        self.ligne = ligne
        self.quartier = quartier
        self.parent = parent

        # On lui defini un QFrame indiquant le prix :    /!\ ajouter les effets aussi
        self.info = QFrame(parent)
        self.info.setStyleSheet("QFrame {background-color:white; color:darkblue}")
        largeur = self.parent.largeur / 2
        hauteur = self.parent.hauteur
        self.info.setGeometry(largeur + 20, 20, largeur / 2 - 40, hauteur - 40)
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

        self.constrPoss  # vaut true si il est constructible sinon vaut false

    def construire(self):
        "Methode du bouton, servant a construire le batiment selectionne"
        if not self.constrPoss:
            return None
        self.parent.ville.construire(self.quartier, self.numBat, self.parent, self.constrPoss)
        # On maj tous les autres batiments
        for i in self.parent.listeBat:
            i.maj()

    def maj(self):
        "methode pour mettre a jour les informations du label"

        # On regarde le cout
        cout = self.parent.ville.cout(self.quartier, self.numBat)
        ressources = ["Argent", "Bois", "Pierre", "Fer", "Or", "Charbon", "Marbre", "Acier", "Nourriture", "Betail", "Chevaux"]
        b = 0
        constr = self.parent.ville.quelleListeDeConstr(self.quartier)
        # On regarde si un batiment est deja en construction
        if constr[0] == self.ligne.numBat:
            self.label[0].setText("Il reste %s tours de construction" % (str(int(constr[1] - constr[2]))))
            b = 1
            self.constrPoss = False  # On dit qu'il ne peut pas etre ameliore
        # On regadre s'il existe un cout (si pas de cout, le batiment est a son nv max)
        elif cout is None:
            self.label[0].setText("Le batiment est a son niveau maximal")
            b = 1
            self.constrPoss = False  # On dit qu'il ne peut pas etre ameliore
        # On regarde si c'est le CV et s'il peut etre ameliore en fonction du niveau de la ville
        elif self.quartier == "CV" and self.numBat == 0 and self.parent.ville.batCV[0] > self.parent.ville.niveauVille:
            self.label[0].setText("La ville nécéssite plus de population pour améliorer le centre-ville")
            b = 1
            self.constrPoss = False
        # On regarde si une autre construction est deja en cours
        elif constr[0] != -1 and constr[0] != self.numBat:
            self.label[0].setText("Une amélioration est déjà en cours dans le quartier")
            b = 1
            self.constrPoss = False
        else:
            self.nvQuart = self.ligne.batQuart[0]
            nvBat = self.ligne.batQuart[self.numBat]
            self.parent.ville.bdd.execute("""SELECT nvQuart FROM Ville WHERE Quartier == "%s" AND Batiment == %s AND Niveau == %s""" % (self.quartier, self.numBat, nvBat + 1))
            self.nvRequis = self.parent.ville.bdd.fetchall()[0][0]
            # On regarde si c'est le bat0 (mais pas du CV)
            if self.numBat == 0 and self.ligne.quartier != "CV":
                # On regarde si on peut l'ameliorer
                if self.parent.ville.batCV[0] < self.nvRequis:
                    self.label[0].setText("Ameliorez le centre-ville pour pouvoir améliorer ce quartier.")
                    b = 1
                    self.constrPoss = False  # On dit qu'il ne peut pas etre ameliore
                else:
                    a = 0
                    # On maj les labels utiles
                    while a < len(ressources):
                        if cout[a + 3] != 0:
                            self.label[b].setText(ressources[a] + " : " + str(cout[a + 3]))
                            self.label[b].show()
                            b += 1
                        a += 1
                    self.constrPoss = True  # On dit qu'il peut etre ameliore
            # On regarde si le batiment est deja a son nv maximum en fonction de son quartier
            elif self.nvQuart < self.nvRequis:
                self.label[0].setText("Ameliorez le quartier pour débloquer de nouveau niveaux.")
                b = 1
                self.constrPoss = False  # On dit qu'il ne peut pas etre ameliore
            else:
                a = 0
                # On maj les labels utiles
                while a < len(ressources):
                    if cout[a + 3] != 0:
                        self.label[b].setText(ressources[a] + " : " + str(cout[a + 3]))
                        self.label[b].show()
                        b += 1
                    a += 1
                self.constrPoss = True  # On dit qu'il peut etre ameliore
        # On cache les labels inutiles
        a = 0
        while a < len(self.label):
            if a >= b:
                self.label[a].hide()
            a += 1

    def enterEvent(self, event):
        self.info.show()

    def leaveEvent(self, event):
        self.info.hide()
